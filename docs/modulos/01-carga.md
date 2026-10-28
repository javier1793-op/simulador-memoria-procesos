# M1 — Carga y validación de procesos

## Qué es
Es la puerta de entrada del simulador. Lee los procesos desde un archivo CSV (o por teclado), revisa que los datos tengan sentido y crea los objetos `Proceso` que usa el resto del programa.

Formato del archivo (`datos/procesos-ejemplo.csv`):
```
id,tamano,arribo,irrupcion
1,200,0,5
```
- **tamano**: en K, lo que ocupa el proceso en memoria.
- **arribo**: instante en que llega al sistema.
- **irrupción** (*burst*): cuánto tiempo de CPU necesita en total.

## Por qué se hizo así
- **CSV**: la consigna dice "leer desde un archivo". CSV se edita con el Bloc de notas o con Excel y es fácil de parsear sin librerías.
- **Validar antes de simular**: si entra un proceso de 500K, nunca va a tener memoria y la simulación **no termina nunca**. Por eso se corta antes, con un mensaje claro.
- **Juntar todos los errores**: si el archivo tiene 3 errores, el usuario los ve todos de una vez, en lugar de corregir uno, volver a ejecutar y encontrarse con el siguiente.
- **Separar `parsear_csv` de `cargar_archivo`**: así se puede testear el parseo con un texto, sin depender de que exista un archivo.
- **Carga manual**: la consigna dice "cargar procesos por parte del usuario".

## Reglas de validación
| Regla | Motivo |
|---|---|
| 1 a 10 procesos | Límite de la consigna |
| id entero, positivo y único | Si dos procesos tienen el mismo id, las tablas son ambiguas |
| 1 ≤ tamaño ≤ 450 | Es toda la memoria de usuario; si no, nunca entra |
| arribo ≥ 0 | No existe el tiempo negativo |
| irrupción ≥ 1 | Un proceso sin tiempo de CPU no tiene sentido |

## Cómo lo implementé
> *(completar al terminar: decisiones, problemas que aparecieron y cómo se resolvieron)*

## Para exponer (1-2 min)
1. Mostrar el CSV de ejemplo y explicar cada columna.
2. Ejecutar con un archivo con errores → mostrar que lista todos los problemas.
3. Explicar por qué un proceso de más de 450K se rechaza (la simulación no terminaría).
4. Mostrar la carga manual.

**Preguntas probables:** *¿Qué pasa si cargo 11 procesos?* · *¿Por qué no aceptás un tamaño de 500K si después se libera memoria?* (porque aunque toda la memoria quede libre son 450K, nunca alcanza).
