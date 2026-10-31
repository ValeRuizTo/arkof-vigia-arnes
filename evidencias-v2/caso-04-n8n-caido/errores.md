# Registro de errores del agente

Lo escriben el agente (cuando el verificador o el revisor rechazan algo), el hook de verificación
(cuando se agotan los reintentos) y el equipo (correcciones manuales). Insumo de la revisión semanal.

| Fecha | Parte | Quién detectó | Error | Corrección / pieza del arnés que se cambió |
|---|---|---|---|---|
| 2026-10-31 | P-V-20261105-1900 | revisor-vigia (ronda 1) | El resumen se apoyaba en `salud` sin citarlo como evidencia; la alerta redondeaba a la baja el plazo vencido de INC-0131 ("hace 3 min" en vez de 3,5) | Se agregó `salud` a la evidencia y la alerta dice "hace más de 3 min". Ronda 2: APROBADO. Sin cambios en el arnés |
| 2026-10-31 | P-V-20261105-1900 | Vigía | El revisor se ejecutó en segundo plano en ambas rondas, aunque triage-ventana exige primer plano; la herramienta lo lanzó así | Se esperó cada veredicto antes de seguir. Pendiente para la revisión del arnés: el agente `revisor-vigia` no se ejecuta en primer plano |
