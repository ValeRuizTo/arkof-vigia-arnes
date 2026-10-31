# Historial de decisiones

Decisiones de criterio que conviene recordar entre sesiones. Una línea: fecha · decisión · razón.

- 2026-10-31 · El SMS desactivado (F-07) se reporta como comportamiento esperado, no como falla · Decisión de diseño del MVP (cap. 8): falta el plan pago de Twilio.
- 2026-10-31 · Telegram cuenta como canal de demostración, no de producción · Requiere datos móviles; no sirve en zonas rurales (cap. 6.4).
- 2026-10-31 · En P-V-20261106-1530, los eventos `confirmado` sin ejecución de n8n se reportan como NUEVA P2 aunque no esté demostrado que el aviso fallara · CLAUDE.md pide reportar como hallazgo la información faltante y, ante la duda, la matriz manda la prioridad más alta; ejemplo-A no lo reporta, así que el criterio sigue por fijar.
- 2026-10-31 · En P-V-20261106-1530, `generado_en` lleva la hora real del reloj aunque sea anterior a la ventana · La ventana es un caso de prueba con fecha futura y otra hora sería inventada.
