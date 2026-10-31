---
name: actualizar-memoria
description: Actualiza la bitácora de progreso, las incidencias abiertas y el historial de decisiones de Vigía al terminar cada parte. Úsala como último paso del triage.
---

# Actualizar la memoria

**Cuándo:** al terminar cada parte (aprobado o no). Solo se escribe en `memoria/`.

## Pasos
1. **`memoria/progreso.md`:** agrega una línea al inicio de la tabla:
   `| <fecha y hora> | <ventana.id> | <estado> | <prioridad máx.> | <causas> | <veredicto verificador> |`
2. **`memoria/incidencias_abiertas.md`:**
   - Causa nueva P1/P2/P3 → agrega una fila con estado `abierta`, primera vez vista y ventana.
   - Causa ya abierta que reaparece → actualiza "última vez vista" y suma 1 a "veces".
   - Causa abierta que **no** aparece y cuya evidencia muestra el canal funcionando → `en observación`;
     tras 2 ventanas limpias seguidas → `resuelta`. Nunca la cierres solo porque no aparece.
3. **`memoria/decisiones.md`:** solo si tomaste una decisión de criterio no obvia (p. ej., "traté el
   error X como NUEVA porque..."). Una línea con fecha, decisión y razón.
4. **`memoria/errores.md`:** si el verificador o el revisor rechazaron algo, registra qué fue y qué
   corregiste. Esto alimenta la revisión semanal del arnés.
5. No copies a la memoria tokens, enlaces de confirmación ni secretos.
