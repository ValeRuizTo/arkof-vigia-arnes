# Registro de errores del agente

Lo escriben el agente (cuando el verificador o el revisor rechazan algo), el hook de verificación
(cuando se agotan los reintentos) y el equipo (correcciones manuales). Insumo de la revisión semanal.

| Fecha | Parte | Quién detectó | Error | Corrección / pieza del arnés que se cambió |
|---|---|---|---|---|
| 2026-10-31 | P-V-20261103-1000 | revisor-vigia (ronda 1) | Bitácora incompleta solo en el resumen semanal; "3 sin responder" sin salvedad; EV-1103 y salud sin citar | Hallazgo NUEVA P3, salvedad en impacto y alerta, evidencia ampliada |
| 2026-10-31 | P-V-20261103-1000 | revisor-vigia (ronda 2) y verificador | Evidencia inexistente `salud.n8n`, introducida al corregir la ronda 1 y no verificada antes de pedir la ronda 2 | Cambiada a `salud`. Sin más rondas: veredicto RECHAZADO, requiere revisión humana. Pieza a revisar: correr el verificador antes de cada ronda; el revisor se lanzó en segundo plano aunque el arnés pide primer plano |
| 2026-10-31T11:10 | P-V-20261103-1000 | hook de verificación | 1 incumplimientos tras 2 reintentos: Los partes con P1/P2 requieren veredicto APROBADO del subagente revisor-vigia. | Pendiente: revisión humana |
