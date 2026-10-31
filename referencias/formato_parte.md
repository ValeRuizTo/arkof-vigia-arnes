# Formato del parte de salud (`partes/P-<id de la ventana>.json`)

```json
{
  "parte_id": "P-V-AAAAMMDD-HHMM",
  "ventana_id": "V-AAAAMMDD-HHMM",
  "ventana_archivo": "casos/.../ventana.json",
  "generado_en": "<fecha y hora ISO>",
  "estado_global": "VERDE | AMARILLO | ROJO",
  "prioridad_maxima": "P1 | P2 | P3 | P4 | null",
  "detectores_disparados": ["D2"],
  "hallazgos": [{
    "causa_catalogo": "F-0X | NUEVA",
    "prioridad": "P1",
    "resumen": "Qué pasa, en una o dos frases, con ids.",
    "evidencia": ["E-0000", "INC-0000"],
    "impacto": "Qué le pasa a una emergencia real por esto.",
    "accion_recomendada": "Qué debe hacer una persona.",
    "requiere_aprobacion_humana": true,
    "es_recurrente": false
  }],
  "comportamientos_esperados": [{"causa_catalogo": "F-07", "nota": "..."}],
  "alerta_coordinador": {"enviar": true, "canal_sugerido": "Telegram / llamada", "texto": "≤ 480 caracteres"},
  "para_resumen_semanal": [],
  "revision": {"revisor": "revisor-vigia", "veredicto": "APROBADO", "archivo": "memoria/revisiones/P-....md"}
}
```
- Sin hallazgos P1/P2: `alerta_coordinador.enviar = false` y `revision.veredicto = "NO_REQUERIDA"`.
- Con P1/P2, mientras el revisor trabaja: `revision.veredicto = "PENDIENTE"`; al recibir su respuesta, `APROBADO` u `OBSERVACIONES`.
- Cada causa raíz aparece **una** vez; sus síntomas van como evidencia del mismo hallazgo.
- Nunca incluyas enlaces de confirmación, contraseñas ni el secreto compartido.
