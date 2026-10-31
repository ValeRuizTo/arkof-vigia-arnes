# Catálogo de fallas conocidas de la cadena de notificación

Cada entrada: firma (cómo se ve en la ventana) → causa probable → acción recomendada.
Todas las acciones las ejecuta una persona; Vigía solo las recomienda.

| Código | Falla | Firma en la ventana | Causa probable | Acción recomendada (humana) | Prioridad base |
|---|---|---|---|---|---|
| F-01 | n8n no recibe eventos | Bandeja con canal `simulación (n8n no respondió)` y error de conexión; sin ejecuciones de n8n en la ventana | n8n detenido, flujo desactivado o URL del webhook errada | Reiniciar o reactivar n8n; mientras tanto activar `VIGILANTE_SLA=1` y llamar por teléfono a las brigadas de los incidentes afectados | P1 |
| F-02 | Verificación del plazo rechazada | Nodo "Verificar plazo en la API" con error 401 | `N8N_SHARED_SECRET` de la app distinto del encabezado `X-ARKOF-Token` del nodo (pasó en la primera ejecución real del MVP) | Igualar el secreto en `.env` y en n8n; revisar manualmente los incidentes `notificado` vencidos | P1 |
| F-03 | Correo no sale por credenciales | Nodos de correo con error `535` / *Username and Password not accepted* | Contraseña de aplicación de Gmail revocada o vencida | Generar una nueva contraseña de aplicación y actualizar la credencial SMTP en n8n; avisar al coordinador por un canal que funcione | P1 si es el único canal de producción |
| F-04 | Telegram rechaza el formato | Error *can't parse entities* | Nodo de Telegram con Markdown y tokens con `_` (ya corregido una vez: usar HTML) | Revisar `parse_mode` HTML en los nodos de Telegram | P3 |
| F-05 | Incidente sin verificación de plazo | Incidente `notificado` más allá del plazo + 3 min sin SLA_VENCIDO/ESCALAMIENTO/BRIGADA_CONFIRMADA | **Síntoma**: búscale la causa (F-01, F-02, Wait detenido). Solo es causa raíz si no hay otra | Revisar el incidente con el coordinador; activar el vigilante interno | P1 |
| F-06 | Entrega lenta | Más de 60 s entre el reporte y la primera entrega por canal de producción | Lentitud o límite de envío del servidor SMTP; n8n sobrecargado | Revisar tiempos de SMTP y cola de n8n; evaluar proveedor de correo transaccional | P2 |
| F-07 | SMS desactivado | Nodos de SMS con estado `disabled` | **Diseño**: falta el plan pago de Twilio | Ninguna: es esperado. Va en `comportamientos_esperados` | — |
| F-08 | Enlaces que no abren desde el celular | `config.public_base_url` con localhost en un entorno compartido; brigadistas que confirman por el portal | `PUBLIC_BASE_URL` sin actualizar tras cambiar de equipo o de túnel ngrok | Actualizar `PUBLIC_BASE_URL` con la URL pública y reiniciar la app | P2 |
| F-09 | Canal de producción falla por otra causa | Error en correo/SMS distinto de 535 | Proveedor caído, límite de cuota, destinatario inválido | Revisar el error con el proveedor | P1 o P2 según cobertura |
