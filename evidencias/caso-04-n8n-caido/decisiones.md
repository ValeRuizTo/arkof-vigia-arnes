# Historial de decisiones

Decisiones de criterio que conviene recordar entre sesiones. Una línea: fecha · decisión · razón.

- 2026-10-31 · El SMS desactivado (F-07) se reporta como comportamiento esperado, no como falla · Decisión de diseño del MVP (cap. 8): falta el plan pago de Twilio.
- 2026-10-31 · Telegram cuenta como canal de demostración, no de producción · Requiere datos móviles; no sirve en zonas rurales (cap. 6.4).
- 2026-10-31 · En P-V-20261103-1000, `generado_en` conserva el reloj real aunque sea anterior a la ventana de prueba · Poner una hora dentro de la ventana sería inventarla.
- 2026-10-31 · En P-V-20261104-1430, la ronda 2 corta de INC-0120 se trató como NUEVA P2, separada de F-03 · El 535 explica por qué no llegan los avisos, no por qué se convocaron 3 con déficit de 5; hubo reasignación, aunque incompleta, y por eso no es P1.
- 2026-10-31 · En P-V-20261104-1430, `generado_en` conserva el reloj real de la versión final, aunque sea anterior a la ventana de prueba · Mismo criterio que P-V-20261103-1000.
- 2026-10-31 · F-02 pasa a `en observación` con V-20261104-1430 · La verificación del plazo respondió sin error en E-7201 a E-7203. Son casos de prueba independientes, así que esto no demuestra que se haya corregido el secreto de V-20261103-1000.
- 2026-10-31 · V-20261105-1900 no cambia el estado de F-02, F-03 ni la NUEVA de V-20261104-1430, ni suma a sus "veces" · Sin ejecuciones de n8n, la ventana no muestra esos pasos funcionando ni fallando; se citan F-02 y F-03 como pendientes que comprobar tras reactivar n8n, no como hallazgos.
