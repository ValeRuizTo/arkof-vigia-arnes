# Cadena de notificación de la plataforma de despacho (MVP ARKOF)

Fuente: capítulos 6 a 8 del documento del proyecto y el repositorio `arkof-despacho-mvp`.

## Componentes y recorrido de un aviso
```
Reporte ─► API Flask + motor de despacho ─► evento JSON al webhook de n8n ─► Switch por tipo de evento
                ▲                                                         ├─ despacho / escalamiento ─► Telegram (demo) · Correo · SMS ─► Wait (plazo) ─► POST verificar-sla
                │                                                         ├─ confirmado ─► Aviso al cliente
                └──────────── POST /api/incidentes/<id>/verificar-sla ◄────┤─ alerta_coordinador ─► Telegram (demo) · Correo · SMS al coordinador
                              (encabezado X-ARKOF-Token = secreto)         └─ cierre ─► Informe de cierre al cliente
```
- La app **no envía mensajes**: publica eventos a n8n (`notificador.py`). Si n8n no responde, la app
  registra el evento en su bandeja con canal `simulación (n8n no respondió)` y el error.
- El **ciclo del plazo** depende de n8n: el nodo Wait espera el plazo (5 min niveles 1-2, 4 min nivel 3)
  y llama a `verificar-sla`, que reemplaza el déficit o escala. Si la verificación falla y el vigilante
  interno (`VIGILANTE_SLA=1`) está apagado, **nadie reasigna** a quien no respondió.
- `/api/salud` responde `n8n: true` cuando `N8N_WEBHOOK_URL` está **configurada**, no cuando n8n está vivo.

## Canales
| Canal | Tipo | Estado en el piloto |
|---|---|---|
| Correo (SMTP Gmail) | Producción | Activo |
| SMS (Twilio) | Producción | **Desactivado por diseño** hasta contratar plan pago (la cuenta gratuita no envía a Colombia) |
| Telegram | Demostración | Activo; requiere datos móviles, no sirve como canal de campo |

Con el SMS desactivado, **el correo es el único canal de producción**. Si el correo cae, los brigadistas
sin datos móviles no reciben la convocatoria.

## Nodos del flujo n8n (13)
Evento ARKOF (webhook) · Tipo de evento (switch) · Un ítem por brigadista · Telegram al brigadista
(demostración) · Correo al brigadista · SMS al brigadista · Esperar plazo de confirmación · Verificar
plazo en la API · Aviso al cliente: brigada en camino · Correo al coordinador · SMS al coordinador ·
Telegram al coordinador (demostración) · Informe de cierre al cliente.
Todos los nodos de envío tienen `onError: continueRegularOutput`: un canal caído no detiene el flujo,
por eso una falla puede pasar **en silencio**.

## Eventos que la app publica
`despacho`, `escalamiento`, `confirmado`, `alerta_coordinador`, `cierre`.

## Tipos de evento en la bitácora
REPORTE · CLASIFICACION · ASIGNACION · RESERVA_EQUIPOS · ALERTA_RECURSOS · NOTIFICACION ·
RESPUESTA_BRIGADISTA · BRIGADA_CONFIRMADA · SIN_REEMPLAZO_NECESARIO · SLA_VENCIDO · ESCALAMIENTO ·
ESCALAMIENTO_HUMANO · CONVOCATORIA_CON_FATIGA · CAMBIO_ESTADO · CIERRE · INFORME.
Estados del incidente: reportado → notificado → confirmado → en_ruta → en_sitio → controlado → cerrado.

## Formato de la ventana de observabilidad
`ventana` (id, desde, hasta, entorno) · `config` (n8n_configurado, sms_habilitado, telegram_demo,
vigilante_sla, public_base_url) · `salud` · `incidentes[]` · `bandeja[]` (ids `B-`) ·
`ejecuciones_n8n[]` (ids `E-`, con el estado y error de cada nodo) · `bitacora[]` (ids `EV-`).
En el MVP la ventana la arma una persona exportando `/api/notificaciones`, `/api/incidentes/<id>` y el
historial de ejecuciones de n8n; en producción la armaría un paso fijo del flujo.

## Glosario
- **Brigada confirmada:** todos los cupos requeridos (total y líderes) confirmaron.
- **Déficit:** cupos sin cubrir contando confirmados y pendientes (RN-08).
- **Plazo / SLA de confirmación:** tiempo máximo para que el brigadista responda (RN-07).
- **Escalamiento humano:** tras 2 rondas automáticas decide el coordinador.
- **Falla silenciosa:** un canal o paso falla sin detener el flujo ni avisar a nadie.
