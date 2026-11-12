# M7 — Salida, estadísticas y entrega

## Qué es
Arma lo que ve el usuario: la pantalla de cada evento, el informe final y el paquete de entrega (ejecutable + HOWTO).

## Lo que pide la consigna en cada evento (llegada o fin de un proceso)
1. **Estado del procesador**: qué proceso está ejecutando (u "ociosa").
2. **Tabla de particiones**: Id · Dirección de comienzo · Tamaño · Proceso asignado · Fragmentación interna.
3. **Colas** de Listos y de Listos/Suspendidos.

Ejemplo de cómo podría verse:
```
══════════ t = 2 │ Llegó: P3 ══════════
CPU: P2 (restante 1)

 Part │ Inicio │ Tamaño │ Proceso │ Frag.Int
──────┼────────┼────────┼─────────┼─────────
  SO  │    0   │  100K  │   SO    │    -
   2  │  100   │  200K  │   P1    │    0K
   3  │  300   │  150K  │   P2    │    0K
   4  │  450   │  100K  │  libre  │    -

Listos:           P1(4)
Listos/Susp.:     P3(3)
Esperando cupo:   —
```

## Informe final
Por proceso: TR y TE, contados desde el ingreso a la cola de Listos (criterio de la cátedra). Además, los promedios y el **rendimiento** (*throughput*) = procesos terminados / tiempo total.

## Por qué se hizo así
- **Las funciones devuelven texto y no hacen `print`**: así se pueden testear, y después se reemplaza la consola por la interfaz con los estilos sin tocar la lógica.
- **Las estadísticas van separadas del render**: el cálculo es lógica del dominio; mostrarlo es presentación.
- **Instalador**: el profe pidió que se lo llevemos con instalador, que lo instale y lo use, **sin instalar nada más y sin internet**. Se arma en dos pasos:
  1. **PyInstaller** mete Python + nuestro código en un solo `simulador.exe`. El profe **no necesita tener Python**.
  2. **Inno Setup** (gratis) envuelve ese `.exe` en `SimuladorSetup.exe`: el clásico Siguiente → Siguiente → Instalar, con accesos directos en el menú Inicio y desinstalador.

  Las dos herramientas sólo se instalan en la PC de quien **construye** el instalador, no en la del profe. Todo está en `instalador/construir.bat` y `instalador/simulador.iss`.

## Cómo construir el instalador
```
pip install pyinstaller
(instalar Inno Setup 6 o 7 desde jrsoftware.org)
instalador\construir.bat      →  instalador\salida\SimuladorSetup.exe
```
**Importante:** probarlo en una PC que **no** tenga Python instalado antes de entregarlo. El antivirus a veces marca los `.exe` de PyInstaller: si pasa, hay que anotarlo en el HOWTO.

El HOWTO para el profe está en `HOWTO.md`, en la raíz del proyecto.

## Cómo lo implementé
**Estadísticas (`estadisticas.py`).** `calcular_estadisticas` recibe la lista de procesos y el tiempo total. Se queda solo con los procesos en estado Terminado, arma una fila por proceso (id, arribo, irrupción, fin, TR y TE) y calcula los promedios y el rendimiento (terminados / tiempo total). Si no hay procesos terminados o el tiempo total es 0, devuelve 0.0 en vez de dividir por cero. El redondeo a 2 decimales no se hace acá sino al mostrar, para no perder precisión.

**Pantallas (`salida.py`).** `render_instante` y `render_informe` solo devuelven texto, sin `print`. Cada evento muestra el encabezado con `t` y lo que ocurrió (llegada, terminación, desalojo), la CPU ("ociosa" si no hay proceso), la tabla de particiones con la fila del SO y las colas de Listos, Listos/Suspendidos y Nuevos esperando cupo. El informe muestra la tabla por proceso, los promedios con 2 decimales y el rendimiento.

**Instalador (`instalador/`).** Se genera con `construir.bat`: PyInstaller empaqueta el simulador en `.exe` (versión con ventana y versión de consola) e Inno Setup arma `SimuladorSetup.exe`, que instala en la carpeta del usuario sin pedir permisos de administrador.

**Problemas que aparecieron y cómo se resolvieron**
- *El comando `pyinstaller` no se reconocía* (el script de PyInstaller no estaba en el PATH). Se usa `python -m PyInstaller`, que anda siempre.
- *Inno Setup 7 se instala en otra ruta que la versión 6*, y el `.bat` no lo encontraba. Se agregó la búsqueda de la ruta de la 7 (hoy el `.bat` prueba la 7 y después la 6).
- *SmartScreen bloquea el instalador* porque los `.exe` no están firmados. Se pasa con "Más información → Ejecutar de todas formas" y quedó escrito en el HOWTO.
- *En una PC con Windows 11 el Control Inteligente de Aplicaciones bloqueó el desinstalador.* En otra PC se desinstaló sin problemas. Se documentó en el HOWTO como algo que puede pasar.

**Pruebas.** Los tests de `tests/test_salida.py` pasan. El instalador se probó en una PC con Windows 11 sin Python: instala, abre la ventana, anda la consola (ejemplo y carga manual) y desinstala bien.

## Para exponer (1-2 min)
1. Recorrer una pantalla de evento explicando cada parte.
2. Mostrar el informe final y explicar TR, TE y rendimiento con un proceso de ejemplo.
3. Mostrar la instalación con `SimuladorSetup.exe` en una PC sin Python.
