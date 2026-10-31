---
name: triage-ventana
description: Analiza una ventana de observabilidad de la plataforma de despacho de ARKOF y produce el parte de salud de la cadena de notificación. Úsala cada vez que te entreguen un ventana.json o pidan revisar la salud de la plataforma.
---

# Triage de una ventana de observabilidad

**Cuándo:** cada ventana nueva (cada 15 min en operación, o a pedido del coordinador).
**Entrada:** ruta a un `ventana.json`. **Salida:** `partes/P-<ventana.id>.json`.

## Pasos
1. **Retoma el contexto.** Lee `memoria/progreso.md` e `memoria/incidencias_abiertas.md`. Anota qué
   incidencias abiertas podrían reaparecer en esta ventana.
2. **Reglas fijas primero.** Corre
   `python3 herramientas/verificar_parte.py --detectores <ventana>` y copia los ids de los detectores
   disparados en `detectores_disparados`. Todo lo que dispare debe quedar cubierto.
3. **Lee la ventana completa** (config, salud, incidentes, bandeja, ejecuciones, bitácora). Busca
   también lo que los detectores no ven: errores no catalogados, nodos que no aparecen, ejecuciones que
   faltan, confirmaciones que llegan por un camino raro (p. ej., portal en vez de enlace).
4. **Agrupa por causa raíz** con `referencias/catalogo_fallas.md`. Pregúntate para cada síntoma:
   "¿esto es consecuencia de otro?". F-05 (incidente atascado) casi siempre es síntoma de F-01 o F-02.
   Un hallazgo por causa; los síntomas van como evidencia (incluye los `INC-` afectados).
5. **Separa lo esperado.** SMS desactivado (F-07) y Telegram como demostración van en
   `comportamientos_esperados`. Un incidente dentro de su plazo no es falla.
6. **Prioriza** con `referencias/matriz_prioridad.md`. Pregunta clave: si ahora entra una emergencia,
   ¿le llega el aviso a la brigada y alguien reasigna a quien no responde? Si la respuesta es no, es P1.
7. **Recomienda sin ejecutar.** Cada acción que cambie algo (reiniciar, reactivar, cambiar credenciales,
   editar `.env`, llamar a brigadistas) lleva `requiere_aprobacion_humana: true`.
8. **Marca recurrencia:** `es_recurrente: true` si la causa ya está en `memoria/incidencias_abiertas.md`.
9. **Alerta:** si hay P1 o P2, usa la skill `redactar-alerta`. Si no, `enviar: false`.
10. **Escribe el parte** en `partes/` con el formato de `referencias/formato_parte.md`.
11. **Revisión:** si hay P1 o P2, invoca al subagente `revisor-vigia` con la ruta de la ventana y del
    parte. Si devuelve OBSERVACIONES, corrige y vuelve a pedir revisión (máximo 2 rondas; si no
    aprueba, deja el parte con veredicto `RECHAZADO` y avisa que necesita revisión humana).
12. **Verifica:** `python3 herramientas/verificar_parte.py <ventana> <parte>` debe decir APROBADO.
    Corrige cada incumplimiento; no lo discutas.
13. Usa la skill `actualizar-memoria`.
