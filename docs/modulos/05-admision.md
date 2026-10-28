# M5 — Admisión: planificadores de largo y mediano plazo

## Qué es
Antes de que un proceso pueda competir por la CPU, alguien tiene que decidir **si entra al sistema** y **si entra a memoria**. De eso se encarga este módulo.

| Planificador | Qué decide | En el simulador |
|---|---|---|
| **Largo plazo** | Qué procesos nuevos se admiten | `admitir_nuevos`: Nuevo → Listo o Listo/Suspendido |
| **Mediano plazo** | Qué procesos suspendidos vuelven a memoria | `promover_suspendidos`: Listo/Susp → Listo |
| **Corto plazo** | Quién usa la CPU | SRTF (módulo M4) |

## Grado de multiprogramación = 5
La consigna dice que **Ejecución + Listo + Listo/Suspendido ≤ 5**. Los Nuevos que no entran **esperan** en estado Nuevo y se vuelven a intentar en cada tick.

```
Llega un proceso ─► ¿hay cupo (< 5)? ─No─► sigue en Nuevo (se reintenta)
                          │Sí
                          ▼
                    ¿Best-Fit encuentra hueco? ─No─► Listo/Suspendido (ocupa cupo, sin memoria)
                          │Sí
                          ▼
                        Listo
```

## Por qué se hizo así
- **`arribo <= t` en vez de `arribo == t`**: con `==`, un proceso que no entró por falta de cupo se perdía para siempre (errores #2 y #3 del diagrama).
- **Primero suspendidos, después nuevos**: los suspendidos llegaron antes. Si los nuevos tuvieran prioridad, podrían quedarse con la memoria una y otra vez y el suspendido nunca entraría (error #4).
- **Orden por arribo**: es FIFO, lo más justo. El orden en el que vienen las filas del archivo no tiene que influir.
- **No bloquear la cola de suspendidos**: si el primero (300K) no entra pero el segundo (100K) sí, se sube el segundo. Así se aprovecha mejor la memoria. Es una **decisión de diseño** que hay que saber defender (la alternativa FIFO estricta es más justa, pero desperdicia memoria).

## Cómo lo implementé
> *(completar)*

## Para exponer (1-2 min)
1. Explicar los 3 niveles de planificación con la tabla.
2. Mostrar el caso del ejemplo: en t=2 P3 (300K) queda Listo/Suspendido porque sólo hay 100K libres.
3. Mostrar el caso con más de 5 procesos: el sexto espera en Nuevo.
