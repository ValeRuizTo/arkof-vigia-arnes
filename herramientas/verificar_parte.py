#!/usr/bin/env python3
"""Verificador de reglas fijas del agente Vigía (capítulo 6 del arnés: sensor).

Dos usos:
  python3 herramientas/verificar_parte.py --detectores <ventana.json>
      Corre los detectores deterministas D1-D8 sobre una ventana de observabilidad
      y muestra qué disparó. El agente lo usa como PRIMER paso (regla fija antes que IA).

  python3 herramientas/verificar_parte.py <ventana.json> <parte.json>
      Verifica un parte de salud contra la ventana. Sale con código 0 si cumple
      todas las reglas y 1 si no, listando cada incumplimiento.

Lo que se puede verificar con una regla fija se verifica aquí. La IA solo juzga
lo que una regla no puede: agrupar síntomas en una causa raíz, distinguir lo
esperado por diseño, priorizar fallas nuevas y redactar la alerta.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

PRIORIDADES = ["P1", "P2", "P3", "P4"]
ESTADOS = {"VERDE", "AMARILLO", "ROJO"}

NODOS_BRIGADISTA_PROD = ["Correo al brigadista", "SMS al brigadista"]
NODOS_COORDINADOR_PROD = ["Correo al coordinador", "SMS al coordinador"]
NODOS_TELEGRAM = ["Telegram al brigadista (demostración)", "Telegram al coordinador (demostración)"]
NODO_VERIFICAR = "Verificar plazo en la API"
EVENTOS_ATENCION_PLAZO = {"SLA_VENCIDO", "ESCALAMIENTO", "ESCALAMIENTO_HUMANO",
                          "BRIGADA_CONFIRMADA", "SIN_REEMPLAZO_NECESARIO"}
MARGEN_PLAZO_MIN = 3
LATENCIA_MAX_S = 60
MAX_TEXTO_ALERTA = 480

PATRONES_SECRETOS = [
    (r"/confirmar/[A-Za-z0-9_\-]{8,}", "token de un enlace de confirmación"),
    (r"\bAC[0-9a-fA-F]{32}\b", "Account SID de Twilio"),
    (r"(?i)auth[_ ]?token\s*[:=]\s*\S+", "Auth Token"),
    (r"(?i)x-arkof-token\s*[:=]\s*\S+", "secreto compartido de n8n"),
    (r"(?i)(contraseña|password|clave)\s*[:=]\s*\S+", "contraseña"),
]
VERBOS_REMEDIACION = r"(?i)\b(reinici|reenvi|forz|reactiv|reimport|rot(ar|e)\b|cambi(ar|e) (el|la) (secreto|contraseña|credencial)|activ(ar|e) VIGILANTE|desactiv)"
ACCIONES_EN_PRIMERA_PERSONA = r"(?i)\b(reinicié|reenvié|forcé|ejecuté|reactivé|reimporté|roté|he (reiniciado|reenviado|forzado|ejecutado|reactivado))\b"


def _t(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def _cargar(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def _causa_por_error(texto):
    t = (texto or "").lower()
    if "535" in t or "username and password" in t or "authentication" in t:
        return "F-03"
    return "F-09"


def detectar(v):
    """Detectores deterministas. Cada uno devuelve una falla con prioridad mínima y evidencia."""
    cfg = v.get("config", {})
    hasta = _t(v["ventana"]["hasta"])
    sms = bool(cfg.get("sms_habilitado"))
    prod_brig = [n for n in NODOS_BRIGADISTA_PROD if sms or not n.startswith("SMS")]
    prod_coord = [n for n in NODOS_COORDINADOR_PROD if sms or not n.startswith("SMS")]
    out = []

    # D1 · n8n no recibe eventos (la app cae a simulación estando n8n configurado)
    ev = [b["id"] for b in v.get("bandeja", []) if str(b.get("canal", "")).startswith("simulación (n8n no respondió)")]
    if ev and cfg.get("n8n_configurado"):
        out.append({"id": "D1", "regla": "n8n no respondió al webhook", "prioridad": "P1", "causa": "F-01", "evidencia": ev})

    ejec = v.get("ejecuciones_n8n", [])
    # D2 · la verificación del plazo es rechazada (401)
    ev = [e["id"] for e in ejec for n in e.get("nodos", [])
          if n["nodo"] == NODO_VERIFICAR and n.get("estado") == "error" and "401" in str(n.get("error"))]
    if ev:
        out.append({"id": "D2", "regla": "verificación del plazo rechazada con 401", "prioridad": "P1", "causa": "F-02", "evidencia": ev})

    # D3 · incidente notificado sin que nadie haya verificado su plazo
    for inc in v.get("incidentes", []):
        if inc.get("estado") != "notificado" or not inc.get("notificado_en"):
            continue
        noti = _t(inc["notificado_en"])
        limite_min = inc.get("sla_minutos", 5) + MARGEN_PLAZO_MIN
        if (hasta - noti).total_seconds() / 60 <= limite_min:
            continue
        atendido = any(e.get("incidente") == inc["codigo"] and e.get("tipo") in EVENTOS_ATENCION_PLAZO
                       for e in v.get("bitacora", []))
        if not atendido:
            out.append({"id": "D3", "regla": f"{inc['codigo']} lleva más de {limite_min} min notificado sin verificación de plazo",
                        "prioridad": "P1", "causa": "F-05", "evidencia": [inc["codigo"]]})

    # D4 / D8 · ningún canal de producción entregó (brigadistas / coordinador)
    for did, eventos, nodos_prod, quien in (("D4", {"despacho", "escalamiento"}, prod_brig, "brigadistas"),
                                             ("D8", {"alerta_coordinador"}, prod_coord, "coordinador")):
        total, parcial = [], []
        causas = set()
        for e in ejec:
            if e.get("evento") not in eventos:
                continue
            nodos = [n for n in e.get("nodos", []) if n["nodo"] in nodos_prod and n.get("estado") != "disabled"]
            fallidos = [n for n in nodos if n.get("estado") == "error"]
            if nodos and len(fallidos) == len(nodos):
                total.append(e["id"])
                causas.update(_causa_por_error(n.get("error")) for n in fallidos)
            elif fallidos:
                parcial.append(e["id"])
                causas.update(_causa_por_error(n.get("error")) for n in fallidos)
        causa = sorted(causas)[0] if causas else "F-09"
        if total:
            out.append({"id": did, "regla": f"ningún canal de producción entregó a {quien}", "prioridad": "P1", "causa": causa, "evidencia": total})
        if parcial:
            out.append({"id": did + "p", "regla": f"falla parcial de un canal de producción hacia {quien}", "prioridad": "P2", "causa": causa, "evidencia": parcial})

    # D5 · latencia reporte → primera entrega por canal de producción
    incs = {i["codigo"]: i for i in v.get("incidentes", [])}
    for e in ejec:
        if e.get("evento") != "despacho" or e.get("incidente") not in incs:
            continue
        exitos = [_t(n["fin"]) for n in e.get("nodos", []) if n["nodo"] in prod_brig and n.get("estado") == "success" and n.get("fin")]
        if not exitos:
            continue
        lat = (min(exitos) - _t(incs[e["incidente"]]["reportado_en"])).total_seconds()
        if lat > LATENCIA_MAX_S:
            out.append({"id": "D5", "regla": f"{e['incidente']}: {lat:.0f} s del reporte a la primera entrega (máx. {LATENCIA_MAX_S} s)",
                        "prioridad": "P2", "causa": "F-06", "evidencia": [e["id"], e["incidente"]]})

    # D6 · canal de demostración (Telegram) con error de formato
    ev = [e["id"] for e in ejec for n in e.get("nodos", [])
          if n["nodo"] in NODOS_TELEGRAM and n.get("estado") == "error" and "parse entities" in str(n.get("error"))]
    if ev:
        out.append({"id": "D6", "regla": "Telegram (demostración) rechazó el formato del mensaje", "prioridad": "P3", "causa": "F-04", "evidencia": ev})

    # D7 · enlaces apuntan a una dirección local en un entorno compartido
    host = urlparse(cfg.get("public_base_url", "")).hostname or ""
    if v["ventana"].get("entorno", "local") != "local" and host in {"localhost", "127.0.0.1", "0.0.0.0"}:
        out.append({"id": "D7", "regla": "PUBLIC_BASE_URL apunta a una dirección local: los enlaces no abren desde el celular",
                    "prioridad": "P2", "causa": "F-08", "evidencia": ["config.public_base_url"]})
    return out


def ids_validos(v):
    ids = {b["id"] for b in v.get("bandeja", [])}
    ids |= {e["id"] for e in v.get("ejecuciones_n8n", [])}
    ids |= {e["id"] for e in v.get("bitacora", [])}
    ids |= {i["codigo"] for i in v.get("incidentes", [])}
    ids |= {f"config.{k}" for k in v.get("config", {})}
    ids.add("salud")
    return ids


def _rango(p):
    return PRIORIDADES.index(p) if p in PRIORIDADES else 99


def verificar(v, parte, raiz=None):
    errores = []
    for campo in ("parte_id", "estado_global", "prioridad_maxima", "hallazgos",
                  "comportamientos_esperados", "alerta_coordinador", "revision"):
        if campo not in parte:
            errores.append(f"Falta el campo obligatorio '{campo}'.")
    if errores:
        return errores

    hall = parte["hallazgos"]
    for i, h in enumerate(hall, 1):
        for campo in ("causa_catalogo", "prioridad", "resumen", "evidencia", "accion_recomendada", "requiere_aprobacion_humana"):
            if campo not in h:
                errores.append(f"Hallazgo {i}: falta '{campo}'.")
        if h.get("prioridad") not in PRIORIDADES:
            errores.append(f"Hallazgo {i}: prioridad '{h.get('prioridad')}' no existe (P1 a P4).")
    if errores:
        return errores

    # Regla 1 · estado global y prioridad máxima coherentes con la matriz
    pmax = min((h["prioridad"] for h in hall), key=_rango, default=None)
    if parte["prioridad_maxima"] != pmax:
        errores.append(f"prioridad_maxima es {parte['prioridad_maxima']} pero la mayor de los hallazgos es {pmax}.")
    esperado = "ROJO" if pmax == "P1" else "AMARILLO" if pmax in ("P2", "P3") else "VERDE"
    if parte["estado_global"] != esperado:
        errores.append(f"estado_global es {parte['estado_global']} pero con prioridad máxima {pmax} debe ser {esperado}.")

    # Regla 2 · cero falsos negativos: todo detector disparado queda cubierto
    for d in detectar(v):
        cubierto = any(_rango(h["prioridad"]) <= _rango(d["prioridad"]) and set(h["evidencia"]) & set(d["evidencia"]) for h in hall)
        if not cubierto:
            errores.append(f"Detector {d['id']} ({d['regla']}, {d['prioridad']}) no está cubierto por ningún hallazgo "
                           f"de prioridad {d['prioridad']} o mayor que cite su evidencia {d['evidencia']}.")

    # Regla 3 · toda evidencia citada existe en la ventana (no inventar)
    validos = ids_validos(v)
    for i, h in enumerate(hall, 1):
        if not h["evidencia"]:
            errores.append(f"Hallazgo {i}: no cita evidencia.")
        for ev in h["evidencia"]:
            if ev not in validos:
                errores.append(f"Hallazgo {i}: la evidencia '{ev}' no existe en la ventana.")

    # Regla 4 · una sola entrada por causa raíz y nada esperado por diseño reportado como falla
    causas = [h["causa_catalogo"] for h in hall if h["causa_catalogo"] != "NUEVA"]
    for c in sorted({c for c in causas if causas.count(c) > 1}):
        errores.append(f"La causa {c} aparece en más de un hallazgo: consolídala en uno solo.")
    if not v.get("config", {}).get("sms_habilitado") and "F-07" in causas:
        errores.append("F-07 (SMS desactivado hasta tener plan pago) es un comportamiento esperado: va en comportamientos_esperados, no como hallazgo.")

    # Regla 5 · sin secretos y sin remediación por cuenta propia
    texto = json.dumps(parte, ensure_ascii=False)
    for patron, nombre in PATRONES_SECRETOS:
        if re.search(patron, texto):
            errores.append(f"El parte contiene un dato protegido ({nombre}). Elimínalo.")
    if re.search(ACCIONES_EN_PRIMERA_PERSONA, texto):
        errores.append("El parte afirma haber ejecutado una acción de remediación. Vigía solo recomienda; no ejecuta.")
    for i, h in enumerate(hall, 1):
        if re.search(VERBOS_REMEDIACION, h["accion_recomendada"]) and not h["requiere_aprobacion_humana"]:
            errores.append(f"Hallazgo {i}: la acción recomendada cambia la plataforma y debe marcarse requiere_aprobacion_humana=true.")

    # Regla 6 · alerta única y corta cuando hay P1 o P2; silencio cuando todo está bien
    al = parte["alerta_coordinador"]
    if pmax in ("P1", "P2"):
        if not al.get("enviar"):
            errores.append("Hay hallazgos P1/P2: alerta_coordinador.enviar debe ser true.")
        if not (1 <= len(al.get("texto", "")) <= MAX_TEXTO_ALERTA):
            errores.append(f"El texto de la alerta debe tener entre 1 y {MAX_TEXTO_ALERTA} caracteres (tiene {len(al.get('texto', ''))}).")
    elif al.get("enviar"):
        errores.append("Sin hallazgos P1/P2 no se envía alerta: los P3/P4 van al resumen semanal.")

    # Regla 7 · revisión independiente obligatoria para P1/P2
    if pmax in ("P1", "P2"):
        rev = parte["revision"]
        if rev.get("revisor") != "revisor-vigia" or rev.get("veredicto") != "APROBADO":
            errores.append("Los partes con P1/P2 requieren veredicto APROBADO del subagente revisor-vigia.")
        elif raiz is not None:
            arch = raiz / rev.get("archivo", "")
            if not arch.is_file() or parte["parte_id"] not in arch.read_text(encoding="utf-8"):
                errores.append(f"No existe la constancia de revisión '{rev.get('archivo')}' escrita por revisor-vigia para {parte['parte_id']}.")
    return errores


def main(argv):
    raiz = Path(__file__).resolve().parents[1]
    if len(argv) == 3 and argv[1] == "--detectores":
        dets = detectar(_cargar(argv[2]))
        if not dets:
            print("Ningún detector disparó.")
        for d in dets:
            print(f"[{d['id']}] {d['prioridad']} · {d['causa']} · {d['regla']} · evidencia: {', '.join(d['evidencia'])}")
        return 0
    if len(argv) != 3:
        print(__doc__)
        return 2
    errores = verificar(_cargar(argv[1]), _cargar(argv[2]), raiz)
    if errores:
        print(f"PARTE RECHAZADO ({len(errores)} incumplimientos):")
        for e in errores:
            print(f"  - {e}")
        return 1
    print("PARTE APROBADO por el verificador de reglas fijas.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
