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
- `parsear_csv` usa `splitlines()` para admitir finales de línea de Windows, ignora líneas vacías y quita espacios. La primera línea no vacía se toma como encabezado. Cada fila debe tener cuatro columnas convertibles a enteros; ante un error de formato se lanza `ErrorCarga` con el número de línea física.
- `validar_procesos` recibe los diccionarios parseados y acumula los errores de cantidad, IDs, tamaño, arribo e irrupción. Una lista vacía genera `No se ingresaron procesos.`. Los errores de formato del parseo detienen la carga en la primera fila incorrecta; la acumulación corresponde a la validación posterior.
- `cargar_archivo` lee UTF-8, parsea y valida antes de crear objetos `Proceso`. Si hay errores de validación, los une con saltos de línea y lanza `ErrorCarga`; `main.py` muestra ese mensaje y termina con código 1. Una carga inválida no se convierte en una lista vacía.
- `carga_manual` vuelve a pedir cada dato inválido y asigna IDs secuenciales desde 1. No implementa el guardado opcional a CSV.

- `validar_procesos` comprueba que cada dato sea realmente un entero: un decimal, un texto, un booleano o un campo ausente se informan como error, sin cortar la validación.

**Verificación:** pasan los 13 tests de M1 (los 11 originales y 2 nuevos, sobre tipos inválidos y valores límite). Los archivos `datos/error-tamano.csv` y `datos/error-varios.csv` muestran los mensajes de error en la demo.

## Para exponer (1-2 min)
1. Mostrar el CSV de ejemplo y explicar cada columna.
2. Ejecutar con un archivo con errores → mostrar que lista todos los problemas.
3. Explicar por qué un proceso de más de 450K se rechaza (la simulación no terminaría).
4. Mostrar la carga manual.

**Preguntas probables:** *¿Qué pasa si cargo 11 procesos?* · *¿Por qué no aceptás un tamaño de 500K si después se libera memoria?* (porque aunque toda la memoria quede libre son 450K, nunca alcanza).
