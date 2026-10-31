# Registro de errores del agente

Lo escriben el agente (cuando el verificador o el revisor rechazan algo), el hook de verificación
(cuando se agotan los reintentos) y el equipo (correcciones manuales). Insumo de la revisión semanal.

| Fecha | Parte | Quién detectó | Error | Corrección / pieza del arnés que se cambió |
|---|---|---|---|---|
| 2026-10-31 | P-V-20261106-1530 | revisor-vigia (ronda 1) | Dejé en `para_resumen_semanal` los eventos `confirmado` sin ejecución (B-602, B-604), sin hallazgo; la alerta y F-08 afirmaban sin matiz que los enlaces no abren | Agregué hallazgo NUEVA P2, gradué F-08 con cupos inferidos, dejé solo llamada como canal y reescribí la alerta. Aprobado en ronda 2 |
| 2026-10-31 | P-V-20261106-1530 | Vigía | El revisor corrió en segundo plano en las dos rondas, aunque la skill triage-ventana exige primer plano | Esperé cada veredicto antes de continuar. Sin cambios en el arnés: la herramienta lanzó al subagente así; el equipo debe revisarlo |
