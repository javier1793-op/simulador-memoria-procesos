# M4 — Planificador de corto plazo SRTF + Gantt

## Qué es
**SRTF** (*Shortest Remaining Time First*) decide **quién usa la CPU** en cada instante: siempre el proceso Listo al que le **falta menos** tiempo de ejecución.

Es **apropiativo** (*preemptive*): si llega un proceso con menos tiempo restante que el que está ejecutando, se lo saca de la CPU (vuelve a Listo **conservando su memoria**) y entra el más corto. Es la versión apropiativa de **SJF**.

## Ejemplo (del caso `datos/procesos-ejemplo.csv`)
- t=0: llega P1 (irrupción 5) → ejecuta P1.
- t=1: llega P2 (irrupción 2). A P1 le quedan 4, y 2 < 4 → **apropiación**: P1 vuelve a Listo y entra P2.

```
Gantt:  | P1 | P2 | P2 | P4 | P1 | P1 | P1 | P1 | P3 | P3 | P3 |
        0    1    2    3    4    5    6    7    8    9    10   11
```

## Por qué se hizo así
- **Apropiación sólo si es ESTRICTAMENTE menor**: si los tiempos empatan, cambiar de proceso no gana nada y sólo agrega un cambio de contexto. Era el error #7 del diagrama.
- **Desempates (menor arribo, después menor id)**: hacen que la simulación sea **determinista** (siempre da el mismo resultado) y que se pueda comparar con los casos resueltos a mano. Priorizar el que llegó antes es lo más justo.
- **Sólo se consideran los Listos**: un Listo/Suspendido no está en memoria, así que no puede ejecutar.
- **CPU ociosa**: si no hay Listos, no se ejecuta nada (error #5 del diagrama).
- **Gantt**: la consigna no lo pide, pero es la mejor forma de *mostrar* SRTF en el video.

## Ventajas y desventajas (para el coloquio)
- ✅ Minimiza el tiempo de espera promedio.
- ❌ Puede generar **inanición** (*starvation*): si siguen llegando procesos cortos, uno largo puede no ejecutar nunca.
- ❌ En un SO real no se conoce de antemano la irrupción (hay que estimarla). En el simulador sí la conocemos porque viene en el archivo.

## Cómo lo implementé
> *(completar)*

## Para exponer (1-2 min)
1. Explicar SRTF y en qué se diferencia de SJF.
2. Mostrar en el Gantt la apropiación de t=1.
3. Explicar la regla de empate y por qué.
4. Mencionar la inanición.
