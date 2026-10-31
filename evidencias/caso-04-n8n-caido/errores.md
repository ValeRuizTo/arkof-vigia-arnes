# Registro de errores del agente

Lo escriben el agente (cuando el verificador o el revisor rechazan algo), el hook de verificación
(cuando se agotan los reintentos) y el equipo (correcciones manuales). Insumo de la revisión semanal.

| Fecha | Parte | Quién detectó | Error | Corrección / pieza del arnés que se cambió |
|---|---|---|---|---|
| 2026-10-31 | P-V-20261103-1000 | revisor-vigia (ronda 1) | Presenté el rechazo de EV-1106 como cupo sin reemplazo, aunque había 5 convocados para 4 cupos. La alerta usaba "18 min sin reasignar" y lenguaje de TI, ambos tomados del ejemplo de `redactar-alerta`. | Parte corregido: el riesgo son los 3 convocados sin respuesta y la alerta dice "plazo vencido hace 13 min". No se cambió el arnés; conviene revisar ese ejemplo. |
| 2026-10-31 | P-V-20261104-1430 | revisor-vigia (ronda 1) | Envié al resumen semanal la ronda 2 que convocó 3 con déficit de 5, con la hipótesis de exportación incompleta, que las cuentas descartan. La nota "Ciclo del plazo" contradecía ese punto y "solo le llegó el Telegram" afirmaba más de lo que muestra la ventana. | Parte corregido: hallazgo NUEVA P2 incluido en la alerta, nota reescrita y "solo salió por el Telegram". No se cambió el arnés. |
| 2026-10-31 | P-V-20261104-1430 | verificar_parte.py | Cité `salud.ok` como evidencia; el verificador solo admite `salud`. | Evidencia cambiada a `salud`. `formato_parte.md` y CLAUDE.md no mencionan ese id: conviene documentarlo. |
| 2026-10-31 | P-V-20261105-1900 | revisor-vigia (ronda 1) | Dije que la ventana no permitía distinguir entre n8n detenido, flujo desactivado o URL errada, aunque `Connection refused` apunta a que nada escuchaba. Mencioné F-03 como pendiente, pero no F-02. | Parte corregido: causa acotada, acción ordenada, comprobación sin 401 y plazo de INC-0131 en la alerta. No se cambió el arnés. Para revisar: con n8n caído, ninguna vía automática lleva la alerta al coordinador y el arnés no define quién hace la llamada. |
