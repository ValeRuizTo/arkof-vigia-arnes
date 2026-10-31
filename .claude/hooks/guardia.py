#!/usr/bin/env python3
"""Hook PreToolUse de Vigía: guardarraíl que vive FUERA del modelo.

Se ejecuta antes de cada herramienta. Si la acción está prohibida sale con código 2:
Claude Code bloquea la herramienta y le muestra al agente el motivo.

Bloquea:
  - Remediación y control de la plataforma (verificar-sla, reinicios, n8n, demo/reiniciar).
  - Llamadas de red y escrituras por shell (Vigía trabaja sobre la ventana exportada y solo escribe con Write).
  - Lectura de secretos (.env) y de las respuestas esperadas de las pruebas (esperado.json).
  - Escribir fuera de partes/ y memoria/ (el agente no puede editar su propio arnés).
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ESCRITURA_PERMITIDA = [RAIZ / "partes", RAIZ / "memoria"]

REGLAS_BASH = [
    (r"verificar-sla|demo/reiniciar|/api/incidentes/\d+/estado|/api/(brigadistas|equipos)/\d+",
     "Es una acción de remediación o un cambio sobre la plataforma. Vigía solo recomienda: déjala en accion_recomendada con requiere_aprobacion_humana=true."),
    (r"iniciar_n8n|\bn8n\s+(start|import|update|execute|export)|\bdocker\b|\bsystemctl\b|\bkill\b|\bpkill\b",
     "Controlar n8n o los servicios requiere aprobación humana. Recomiéndalo en el parte."),
    (r"\bcurl\b|\bwget\b|requests\.(get|post|put|patch|delete)|\bhttpx\b|urllib\.request|Invoke-WebRequest|\bnc\b",
     "Vigía no hace llamadas de red: trabaja solo sobre la ventana de observabilidad exportada."),
    (r"esperado\.json",
     "esperado.json contiene las respuestas de las pruebas del equipo; leerlo invalida la prueba."),
    (r"\.env(?![\w.])",
     "El archivo .env tiene secretos; Vigía no lo lee. Usa el bloque config de la ventana."),
    (r"(^|[;&|]\s*)(rm|mv|cp|chmod|truncate)\b|\bsed\s+-i|\btee\b|>\s*[^&\s]|>>|git\s+(push|commit|reset|checkout|clean|restore)",
     "Vigía no modifica archivos por shell. Escribe el parte y la memoria solo con la herramienta Write."),
    (r"\b(pip|npm|apt|brew)\s+install\b",
     "Vigía no instala paquetes."),
]


def bloquear(motivo):
    print(f"BLOQUEADO por el guardarraíl de Vigía: {motivo}", file=sys.stderr)
    sys.exit(2)


def dentro(ruta, carpetas):
    try:
        r = Path(ruta).resolve()
    except Exception:
        return False
    return any(r == c or c in r.parents for c in carpetas)


def main():
    try:
        datos = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    herramienta = datos.get("tool_name", "")
    entrada = datos.get("tool_input", {}) or {}
    cwd = Path(datos.get("cwd") or RAIZ)

    if herramienta == "Bash":
        cmd = entrada.get("command", "")
        for patron, motivo in REGLAS_BASH:
            if re.search(patron, cmd):
                bloquear(motivo)

    elif herramienta in ("Read", "NotebookRead"):
        ruta = str(entrada.get("file_path", ""))
        if ruta.endswith("esperado.json"):
            bloquear(REGLAS_BASH[3][1])
        if re.search(r"\.env$", ruta):
            bloquear(REGLAS_BASH[4][1])

    elif herramienta == "Grep":
        objetivo = Path(entrada.get("path") or cwd)
        objetivo = objetivo if objetivo.is_absolute() else (cwd / objetivo)
        glob = str(entrada.get("glob", ""))
        if "esperado" in glob or str(objetivo).endswith("esperado.json"):
            bloquear(REGLAS_BASH[3][1])
        if objetivo.is_dir() and not glob and (objetivo.resolve() == RAIZ or "casos" in objetivo.resolve().parts):
            bloquear("Una búsqueda sin filtro alcanzaría casos/*/esperado.json. Usa glob='ventana.json' o la ruta de un archivo.")

    elif herramienta in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        ruta = entrada.get("file_path") or entrada.get("notebook_path") or ""
        ruta = ruta if Path(ruta).is_absolute() else str(cwd / ruta)
        if not dentro(ruta, ESCRITURA_PERMITIDA):
            bloquear(f"Solo puedes escribir en partes/ y memoria/. '{ruta}' está fuera: el agente no edita su propio arnés, el código ni la configuración.")

    elif herramienta in ("WebFetch", "WebSearch"):
        bloquear(REGLAS_BASH[2][1])

    sys.exit(0)


if __name__ == "__main__":
    main()
