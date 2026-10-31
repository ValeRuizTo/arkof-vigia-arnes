---
name: redactar-alerta
description: Redacta la única alerta al coordinador HSE de ARKOF cuando un parte de salud tiene hallazgos P1 o P2. Úsala dentro del triage, después de priorizar.
---

# Redactar la alerta al coordinador

**Cuándo:** el parte tiene al menos un hallazgo P1 o P2. **Salida:** `alerta_coordinador` del parte.

## Pasos
1. **Una sola alerta** para toda la ventana, aunque haya varias causas: empieza por la más grave.
2. **Estructura (≤ 480 caracteres, cabe en un SMS largo o en Telegram):**
   `[ARKOF·Vigía] <P1/P2> <qué falla, en palabras del coordinador>. Afecta: <INC- afectados o "próximos despachos">. Haga ya: <acción operativa inmediata>. Admin TI: <acción técnica>.`
3. **Lenguaje del coordinador, no de TI:** "las brigadas no están recibiendo el correo de
   convocatoria", no "nodo emailSend con 535".
4. **Cifras que el coordinador usa:** minutos desde que venció el plazo y cuántos convocados faltan por
   responder frente a los cupos requeridos (ver "Déficit" en `referencias/cadena_notificacion.md`).
5. **Acción operativa primero:** lo que el coordinador puede hacer ya para proteger la emergencia
   (llamar a la brigada del incidente afectado, revisar a mano los incidentes vencidos). La técnica va después.
6. **Canal sugerido que funcione:** nunca sugieras el canal que está caído. Si el correo falla,
   sugiere Telegram o llamada; si n8n está caído, llamada telefónica (n8n envía todas las alertas).
7. **Prohibido en el texto:** enlaces de confirmación, tokens, contraseñas, secretos, y frases que
   afirmen que Vigía ya hizo algo ("reinicié", "reenvié").
8. Cuenta los caracteres antes de escribir. Si pasa de 480, recorta la parte técnica, nunca la operativa.

## Ejemplo (escenario ficticio, no es un caso de prueba)
`[ARKOF·Vigía] P1 Las brigadas no están recibiendo la convocatoria por ningún canal. Afecta: INC-0077 (plazo vencido hace 4 min, 3 de 4 sin responder) y próximos despachos. Haga ya: llame a la brigada de INC-0077 y despache por teléfono mientras se corrige. Admin TI: revisar el estado y el saldo del proveedor de mensajería.`

Fíjate en lo que hace bien: dice qué le pasa a la operación (no qué nodo falló), cuenta el tiempo desde
que **venció el plazo** (no desde la notificación), dice **cuántas personas faltan** por responder y
pone primero lo que el coordinador puede hacer ya.
