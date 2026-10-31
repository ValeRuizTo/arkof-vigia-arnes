# Matriz de prioridad de Vigía

La prioridad se decide por el **impacto sobre una emergencia real**, no por el número de errores.

| Prioridad | Cuándo | Ejemplos | Qué hace Vigía |
|---|---|---|---|
| **P1 · Crítica** | Un aviso de emergencia puede no llegar o nadie reasigna a quien no respondió | n8n no recibe eventos; ningún canal de producción entrega a brigadistas o al coordinador; la verificación del plazo falla; un incidente sigue `notificado` más allá del plazo + 3 min sin SLA_VENCIDO, ESCALAMIENTO ni BRIGADA_CONFIRMADA | Estado ROJO · alerta inmediata · revisión obligatoria |
| **P2 · Alta** | La cadena funciona pero degradada: el aviso llega tarde o con fricción | Latencia reporte → primera entrega > 60 s; un canal de producción falla en parte; enlaces que no abren desde el celular; falla el aviso o el informe al cliente | Estado AMARILLO · alerta · revisión obligatoria |
| **P3 · Media** | Falla sin efecto sobre la atención | Error en Telegram (demostración); error aislado que se recuperó solo | Estado AMARILLO · sin alerta · va al resumen semanal |
| **P4 · Baja** | Observación o mejora | Variación menor de tiempos dentro de la meta | Estado VERDE · resumen semanal |

**Estado global:** ROJO si hay algún P1; AMARILLO si la mayor es P2 o P3; VERDE si no hay hallazgos o solo P4.

**Reglas de juicio**
- Varios síntomas con la misma causa raíz son **un** hallazgo con la prioridad del síntoma más grave
  (p. ej., un 401 en la verificación y el incidente que por eso quedó sin reasignar).
- Lo que está así por diseño (SMS desactivado, Telegram como demostración) va en
  `comportamientos_esperados`, nunca como hallazgo.
- Un incidente en curso dentro de su plazo no es falla.
- Una falla de un canal de producción cuando es el **único** activo cuenta como "ningún canal entregó".
- Si la causa no está en el catálogo, usa `NUEVA` y descríbela con la evidencia; no la fuerces a una conocida.
- Ante la duda entre dos prioridades, la más alta: es peor callar una caída que alertar de más.
