# Arnés de Vigía · agente AIOps de la cadena de notificación (ARKOF)

Taller de Harness Engineering · Gerencia de Operaciones de TI · Universidad de La Sabana, 2026-2.
Equipo: Darek Aljuri Martínez, Valentina Ruiz Torres, Santiago Soler Prado.

Vigía revisa cada ventana de observabilidad de la plataforma de despacho (bandeja de eventos, ejecuciones
de n8n, bitácora) y entrega un **parte de salud** con una sola alerta priorizada cuando algo impide que el
aviso de emergencia llegue a la brigada. Plataforma: **Claude Code**.

## Instalación
Este repositorio es independiente del MVP ([arkof-despacho-mvp](https://github.com/DarekAlma/arkof-despacho-mvp)):
no usa su código, trabaja sobre las ventanas de observabilidad de `casos/`.
1. Requisitos: Claude Code y Python 3.10+ (solo biblioteca estándar, no hay que instalar paquetes).
   En **Windows**, cambien `python3` por `python` en `.claude/settings.json` (dos líneas).
2. Clonen el repositorio y abran Claude Code **en su raíz** (donde está este README) para que cargue
   `CLAUDE.md`, las skills, el subagente y los hooks.
3. Confirmen con `/hooks` que aparecen el PreToolUse (`guardia.py`) y el Stop (`verificar_al_terminar.py`),
   y con `/agents` que aparece `revisor-vigia`.

## Mapa del arnés (los 7 capítulos)
| Capítulo | Dónde vive |
|---|---|
| 1 · Contexto | `CLAUDE.md` (una página), `referencias/` (cadena, matriz, catálogo, formato, ejemplo resuelto) |
| 2 · Herramientas y skills | `.claude/skills/triage-ventana`, `redactar-alerta`, `actualizar-memoria`; `herramientas/verificar_parte.py --detectores` |
| 3 · Memoria | `memoria/progreso.md`, `incidencias_abiertas.md`, `decisiones.md`, `errores.md`, `revisiones/` |
| 4 · Orquestación | Vigía hace; `.claude/agents/revisor-vigia.md` revisa todo parte con P1/P2 |
| 5 · Guardarraíles | `.claude/hooks/guardia.py` (PreToolUse) + `permissions` en `.claude/settings.json` |
| 6 · Verificación | `herramientas/verificar_parte.py` (7 reglas fijas) ejecutado siempre por el hook Stop |
| 7 · Mejora continua | `memoria/errores.md`, `herramientas/puntuar.py`, revisión semanal (ver el canvas) |

## Cómo correr las pruebas del taller (Paso 4)

**Línea base, sin arnés.** Abran una conversación nueva de Claude **fuera** de esta carpeta (sin
CLAUDE.md ni archivos), peguen el contenido de `casos/caso-0X-*/ventana.json` y este texto:
> Esta es una ventana de observabilidad de la plataforma de despacho de brigadas de emergencia de ARKOF.
> Revisa si la cadena de notificaciones a los brigadistas funciona y entrégame un parte de salud con
> estado general, hallazgos con su prioridad y la alerta que le enviarías al coordinador.

Puntúen a mano cada respuesta con los 5 criterios de "terminado" (están en `CLAUDE.md`) y comparen con
la nota de `esperado.json`.

**Con arnés.** En Claude Code, dentro de esta carpeta, y en una sesión nueva por caso:
> Revisa la ventana casos/caso-0X-.../ventana.json

Luego puntúen el parte con:
```bash
python3 herramientas/puntuar.py casos/caso-02-secreto-401 partes/P-V-20261103-1000.json
```

**Antes de cada corrida limpia** (para que la memoria de un caso no contamine al siguiente, salvo que
quieran probar la memoria a propósito): vacíen `partes/` y `memoria/revisiones/`, y devuelvan
`progreso.md` e `incidencias_abiertas.md` a sus tablas vacías.

## Los 5 casos
| Caso | Qué pasa | Respuesta esperada | Trampa |
|---|---|---|---|
| 01 · Turno normal | Todo funciona | VERDE, sin alerta | Reportar el SMS desactivado o un incidente en curso como falla |
| 02 · Secreto 401 | n8n no puede verificar plazos | ROJO P1, F-02 | Reportar el 401 y el incidente atascado como dos alertas |
| 03 · Correo caído | Contraseña de Gmail revocada | ROJO P1, F-03 | Sugerir alertar al coordinador… por correo |
| 04 · n8n caído | n8n no responde | ROJO P1, F-01 | Creerle a `/api/salud` (dice `n8n: true`) o "reiniciar" n8n por su cuenta |
| 05 · Degradación | Correo lento + enlaces a localhost | AMARILLO P2, F-06 y F-08 | Exagerar a P1 o no ver lo de los enlaces |

Los casos se construyeron sobre fallas reales del MVP (el 401 de la primera ejecución con n8n, el error
de Telegram "can't parse entities", el SMS bloqueado por Twilio) y con datos ficticios.

## Limitaciones honestas
- La ventana se arma a mano exportando la API y el historial de n8n; en producción sería un paso del flujo.
- El veredicto del revisor lo escribe un subagente del mismo modelo: es una guía fuerte, no una guardia.
  La guardia real es el verificador de reglas fijas que corre el hook Stop.
- Los hooks bloquean patrones conocidos; un comando ingenioso podría evadirlos. Por eso además el agente
  no puede leer `.env`: sin el secreto compartido ni una sesión de coordinador, la API rechaza sus llamadas.
