# Registro de errores del agente

Lo escriben el agente (cuando el verificador o el revisor rechazan algo), el hook de verificación
(cuando se agotan los reintentos) y el equipo (correcciones manuales). Insumo de la revisión semanal.

| Fecha | Parte | Quién detectó | Error | Corrección / pieza del arnés que se cambió |
|---|---|---|---|---|
| 2026-10-31 | P-V-20261104-1430 | revisor-vigia (ronda 1) | Anomalía de la ronda 2 (3 convocados con déficit 5) enviada solo al resumen semanal; frase que sugería respaldo del vigilante apagado; Telegram etiquetado NUEVA en comportamientos esperados | Hallazgo NUEVA P1 con evidencia y mención en la alerta; frase eliminada; causa_catalogo null en Telegram. Sin cambios en el arnés |
| 2026-10-31 | P-V-20261104-1430 | Agente | revisor-vigia se lanzó en segundo plano aunque la skill exige primer plano: la herramienta no ofrece esa opción | No se avanzó hasta recibir cada veredicto. Pendiente de revisar la instrucción en triage-ventana. Sin cambios en el arnés |
