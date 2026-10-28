# M3 — Memoria con particiones variables (MVT) y Best-Fit

## Qué es
Simula la memoria principal: **550K** en total, de los cuales **100K** son del SO (direcciones 0–99) y **450K** quedan para los procesos (direcciones 100–549).

Con **MVT** (*Multiprogramming with a Variable number of Tasks*) **no hay particiones fijas de antemano**: cuando entra un proceso se crea una partición **del tamaño exacto** que necesita.

```
Al inicio:        |  SO 100K  |              libre 450K                     |
Entra P1 (200K):  |  SO 100K  |  P1 200K  |          libre 250K             |
Entra P2 (150K):  |  SO 100K  |  P1 200K  |  P2 150K  |  libre 100K          |
Sale P1:          |  SO 100K  | libre 200K|  P2 150K  |  libre 100K          |  ← fragmentación externa
```

## Best-Fit
Entre todos los huecos libres que alcanzan, se elige **el más chico**. La idea es que el sobrante sea lo menor posible y que los huecos grandes queden disponibles para procesos grandes.
- Comparación: *First-Fit* toma el primero que alcanza (es más rápido); *Worst-Fit* toma el más grande.
- Desempate (decisión nuestra): si dos huecos miden lo mismo, se elige el de menor dirección.

## Por qué se hizo así
- **Lista ordenada por dirección**: así es fácil mostrar la tabla y encontrar a los vecinos al liberar.
- **Fusionar al liberar** (*coalescing*): si quedan dos huecos de 100K pegados y no se fusionan, un proceso de 150K no entra aunque haya 200K libres contiguos. Era el error #8 del diagrama.
- **No compactamos**: la consigna no lo pide, y mover procesos en memoria tiene un costo. Lo explicamos como posible mejora.

## Fragmentación (pregunta segura del coloquio)
- **Interna**: espacio desperdiciado *dentro* de una partición asignada. En MVT es **0**, porque la partición se crea del tamaño exacto. La columna se muestra porque la consigna la pide.
- **Externa**: memoria libre total suficiente, pero repartida en huecos que por separado no alcanzan. **Es el problema típico de MVT**, y se ve en la simulación cuando un proceso queda Listo/Suspendido aunque la suma de los huecos alcanzaría.

## Cómo lo implementé
> *(completar)*

## Para exponer (1-2 min)
1. Dibujar la memoria y mostrar una asignación (partir el hueco).
2. Mostrar un caso donde Best-Fit elige un hueco distinto al que elegiría First-Fit.
3. Mostrar una liberación con fusión de huecos.
4. Explicar por qué la fragmentación interna da 0 y señalar un caso de fragmentación externa.
