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
4. **Acción operativa primero:** lo que el coordinador puede hacer ya para proteger la emergencia
   (llamar a la brigada de INC-0110, revisar a mano los incidentes vencidos). La técnica va después.
5. **Canal sugerido que funcione:** nunca sugieras el canal que está caído. Si el correo falla,
   sugiere Telegram o llamada; si n8n está caído, llamada telefónica (n8n envía todas las alertas).
6. **Prohibido en el texto:** enlaces de confirmación, tokens, contraseñas, secretos, y frases que
   afirmen que Vigía ya hizo algo ("reinicié", "reenvié").
7. Cuenta los caracteres antes de escribir. Si pasa de 480, recorta la parte técnica, nunca la operativa.

## Ejemplo
`[ARKOF·Vigía] P1 El escalamiento automático no funciona: n8n no puede verificar los plazos (credencial rechazada). Afecta: INC-0110, 18 min sin reasignar. Haga ya: llame a la brigada de INC-0110 y revise a mano los incidentes notificados. Admin TI: igualar el secreto compartido entre la app y n8n.`
