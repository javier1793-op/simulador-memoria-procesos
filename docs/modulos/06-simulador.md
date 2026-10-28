# M6 — Motor de simulación (reloj e integración)

## Qué es
Es el "director de orquesta": maneja el reloj `t` y en cada tick llama a los demás módulos **en un orden fijo**. Por sí solo no decide nada de memoria ni de CPU: delega en los otros módulos.

## El ciclo de un tick (el orden importa)
```
en el instante t:
  1. promoverSuspendidos     (mediano plazo — M5)
  2. admitirNuevos           (largo plazo — M5)
  3. planificar SRTF         (corto plazo — M4)
  4. si hubo arribo o fin  → mostrar estado y PAUSA (M7)
  5. ejecutar 1 unidad       (restante − 1; Gantt)
  6. si restante = 0       → Terminado, fin = t+1, liberar memoria (M3)
  7. t = t + 1
```
**Por qué este orden:** la memoria se reparte *antes* de que SRTF decida (así un proceso que acaba de llegar ya puede competir), y la pantalla se muestra *antes* de ejecutar (refleja quién va a usar la CPU en ese instante).

## Separación motor / pantalla
`Simulador.paso()` **no imprime nada**: devuelve una `Instantanea` (objeto con todo el estado). `main.py` decide si la muestra y espera el Enter. Gracias a esto:
- se puede testear sin intervención (`tests/test_integracion.py`),
- después se puede reemplazar la consola por la interfaz con los estilos **sin tocar el motor**.

## Ejemplo resuelto a mano (`datos/procesos-ejemplo.csv`)
| Proceso | Tamaño | Arribo | Irrupción |
|---|---|---|---|
| P1 | 200K | 0 | 5 |
| P2 | 150K | 1 | 2 |
| P3 | 300K | 2 | 3 |
| P4 | 50K | 3 | 1 |

| t | Qué pasa | Memoria (usuario) | CPU |
|---|---|---|---|
| 0 | Llega P1 → Listo | P1[100-299] libre 250 | P1 |
| 1 | Llega P2 → Listo. 2 < 4 → **apropiación** | P1, P2[300-449], libre 100 | P2 |
| 2 | Llega P3 (300K): no entra → **Listo/Susp** | igual | P2 |
| 3 | Termina P2 (libera y fusiona → libre 250). P3 sigue sin entrar. Llega P4 → Listo | P1, P4[300-349], libre 200 | P4 |
| 4 | Termina P4 (libre 250) | P1, libre 250 | P1 |
| 8 | Termina P1 → todo libre (450) → P3 sube a Listo | P3[100-399], libre 150 | P3 |
| 11 | Termina P3. Fin | todo libre | — |

| Proceso | Fin | TR = fin − arribo | TE = TR − irrupción |
|---|---|---|---|
| P1 | 8 | 8 | 3 |
| P2 | 3 | 2 | 0 |
| P3 | 11 | 9 | 6 |
| P4 | 4 | 1 | 0 |
| **Promedio** | | **5,00** | **2,25** |

Rendimiento = 4 procesos / 11 unidades = **0,36 procesos por unidad de tiempo**.

## Cómo lo implementé
> *(completar)*

## Para exponer (2-3 min, es la demo principal)
1. Explicar el ciclo de un tick y por qué en ese orden.
2. Ejecutar `python main.py datos\procesos-ejemplo.csv` (o el .exe instalado) y avanzar con Enter comentando cada evento contra la tabla de arriba.
3. Explicar la pausa: la consigna prohíbe corridas ininterrumpidas.
4. Mostrar todos los tests en verde: `python -m unittest discover -s tests -v`.
