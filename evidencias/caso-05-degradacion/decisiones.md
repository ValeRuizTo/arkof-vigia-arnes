# Historial de decisiones

Decisiones de criterio que conviene recordar entre sesiones. Una línea: fecha · decisión · razón.

- 2026-10-31 · El SMS desactivado (F-07) se reporta como comportamiento esperado, no como falla · Decisión de diseño del MVP (cap. 8): falta el plan pago de Twilio.
- 2026-10-31 · Telegram cuenta como canal de demostración, no de producción · Requiere datos móviles; no sirve en zonas rurales (cap. 6.4).
- 2026-10-31 · Un evento confirmado sin ejecución de n8n en la ventana se trató como NUEVA P2, declarado como información faltante y no como falla comprobada · La bandeja solo prueba que el evento se publicó; la matriz lista la falla del aviso al cliente como P2 y manda elegir la prioridad más alta ante la duda. El parte de ejemplo-A calla sobre la misma forma: el equipo debe definir si esa ausencia es aceptable.
- 2026-10-31 · En P-V-20261106-1530, generado_en conserva el reloj real del sistema aunque es anterior a ventana.desde · La ventana es un caso de prueba con fechas futuras y no se deben inventar horas.
