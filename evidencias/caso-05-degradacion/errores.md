# Registro de errores del agente

Lo escriben el agente (cuando el verificador o el revisor rechazan algo), el hook de verificación
(cuando se agotan los reintentos) y el equipo (correcciones manuales). Insumo de la revisión semanal.

| Fecha | Parte | Quién detectó | Error | Corrección / pieza del arnés que se cambió |
|---|---|---|---|---|
| 2026-10-31 | P-V-20261106-1530 | revisor-vigia (ronda 1) | Aviso al cliente sin constancia priorizado como P4 apoyándose en el silencio de ejemplo-A; alerta que generalizaba "los enlaces no abren" y ordenaba corregir PUBLIC_BASE_URL sin revisar el túnel; faltaba declarar el vacío de respuestas en la bitácora | Subió a P2 con comprobación ante el cliente; alerta reescrita; vacío declarado en F-08. Aprobado en ronda 2. Sin cambios en el arnés |
| 2026-10-31 | P-V-20261106-1530 | Vigía (proceso) | revisor-vigia se ejecutó en segundo plano en ambas rondas, aunque la skill triage-ventana pide primer plano; la herramienta Agent no ofrece esa opción en esta sesión | Se esperó cada veredicto antes de continuar. Revisar la instrucción de la skill o la definición del subagente |
