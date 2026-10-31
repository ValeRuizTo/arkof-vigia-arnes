#!/usr/bin/env python3
"""Hook Stop de Vigía: verificación que SIEMPRE ocurre antes de entregar.

Cuando el agente intenta terminar, busca el parte escrito en los últimos 30 minutos y lo pasa por el
verificador de reglas fijas. Si falla, sale con código 2: el agente no puede terminar y recibe la lista
de incumplimientos para corregirlos.

Límite de reintentos: tras 2 rechazos del mismo parte deja terminar, pero marca el parte como
RECHAZADO (partes/<id>.RECHAZADO.txt), lo registra en memoria/errores.md y avisa que necesita
revisión humana. Así un parte malo nunca sale como si estuviera bien y el agente no queda en bucle.
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "herramientas"))
import verificar_parte as V  # noqa: E402

MAX_REINTENTOS = 2
VENTANA_S = 30 * 60
CONTADOR = RAIZ / ".claude" / "hooks" / ".intentos.json"


def leer_contador():
    try:
        return json.loads(CONTADOR.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main():
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    partes = sorted((p for p in (RAIZ / "partes").glob("P-*.json") if time.time() - p.stat().st_mtime < VENTANA_S),
                    key=lambda p: p.stat().st_mtime, reverse=True)
    if not partes:
        sys.exit(0)
    ruta = partes[0]
    contador = leer_contador()
    clave = f"{ruta.name}:{int(ruta.stat().st_mtime)}"

    parte = {}
    try:
        parte = json.loads(ruta.read_text(encoding="utf-8"))
        ventana_rel = parte.get("ventana_archivo")
        if not ventana_rel or not (RAIZ / ventana_rel).is_file():
            errores = [f"ventana_archivo ('{ventana_rel}') debe ser la ruta, relativa a la carpeta del arnés, de la ventana analizada."]
        else:
            ventana = json.loads((RAIZ / ventana_rel).read_text(encoding="utf-8"))
            errores = V.verificar(ventana, parte, RAIZ)
    except json.JSONDecodeError as e:
        errores = [f"{ruta.name} no es JSON válido: {e}"]

    estado = contador.get(ruta.name, {"rechazos": 0, "reportado": False})
    # Un parte que espera al revisor no está terminado ni fallido: no gasta reintentos y no se marca RECHAZADO.
    if errores and parte.get("revision", {}).get("veredicto") == "PENDIENTE":
        print(json.dumps({"systemMessage": f"Vigía: el parte {ruta.name} sigue PENDIENTE de revisión; "
                                           "no está entregado hasta que revisor-vigia dé su veredicto y pase el verificador."}))
        sys.exit(0)
    if not errores:
        contador.pop(ruta.name, None)
        CONTADOR.write_text(json.dumps(contador), encoding="utf-8")
        (RAIZ / "partes" / f"{ruta.stem}.RECHAZADO.txt").unlink(missing_ok=True)
        sys.exit(0)

    if estado["rechazos"] < MAX_REINTENTOS:
        estado["rechazos"] += 1
        estado["ultima_clave"] = clave
        contador[ruta.name] = estado
        CONTADOR.write_text(json.dumps(contador), encoding="utf-8")
        print(f"El parte {ruta.name} NO pasó el verificador (intento {estado['rechazos']} de {MAX_REINTENTOS}). "
              "Corrige y vuelve a escribirlo antes de terminar:\n- " + "\n- ".join(errores), file=sys.stderr)
        sys.exit(2)

    if not estado.get("reportado"):
        (RAIZ / "partes" / f"{ruta.stem}.RECHAZADO.txt").write_text(
            "PARTE RECHAZADO tras agotar los reintentos. Requiere revisión humana.\n- " + "\n- ".join(errores), encoding="utf-8")
        with open(RAIZ / "memoria" / "errores.md", "a", encoding="utf-8") as f:
            f.write(f"| {datetime.now().isoformat(timespec='minutes')} | {ruta.stem} | hook de verificación | "
                    f"{len(errores)} incumplimientos tras {MAX_REINTENTOS} reintentos: {errores[0][:120]} | Pendiente: revisión humana |\n")
        estado["reportado"] = True
        contador[ruta.name] = estado
        CONTADOR.write_text(json.dumps(contador), encoding="utf-8")
    print(json.dumps({"systemMessage": f"Vigía: el parte {ruta.name} quedó RECHAZADO tras {MAX_REINTENTOS} reintentos y requiere revisión humana."}))
    sys.exit(0)


if __name__ == "__main__":
    main()
