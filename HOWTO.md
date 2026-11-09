# HOWTO — Cómo instalar y usar el simulador

## Instalación (no requiere Python ni internet)
1. Ejecutar `SimuladorSetup.exe`.
2. Siguiente → Siguiente → Instalar. No pide permisos de administrador: se instala en `C:\Users\<usuario>\AppData\Local\Programs\SimuladorSO`.
3. Queda en el menú Inicio: **Simulador** (con ventana) y **Simulador en consola** (ejemplo y carga manual). También se crea un acceso **Simulador SO** en el escritorio, que abre la versión con ventana.
4. Los archivos CSV de prueba quedan en la carpeta `datos` de la instalación (`procesos-ejemplo.csv`, `error-tamano.csv` y `error-varios.csv`).

## Uso
**Con ventana** (`simulador.exe`): abre con el ejemplo cargado.
- **Siguiente evento** (o Enter) avanza hasta que llega o termina un proceso.
- Al terminar todos los procesos aparece el informe final y el botón **Siguiente evento** se desactiva.
- **Abrir CSV** carga otro archivo y **Carga manual** permite escribir los procesos.
- **Reiniciar** vuelve a empezar con los mismos procesos.

**En consola** (`simulador-consola.exe`):
- **Con archivo**: `simulador-consola.exe ruta\al\archivo.csv`
- **Carga manual**: abrirlo sin parámetros y responder lo que pide.
- En cada evento la simulación se detiene: presionar **Enter** para continuar.
- Al final muestra el informe y espera un **Enter** para cerrarse, así se puede leer con calma.

## Formato del archivo
```
id,tamano,arribo,irrupcion
1,200,0,5
2,150,1,2
```
Máximo 10 procesos. El tamaño se expresa en K y no puede superar 450. Si el archivo tiene errores, el simulador los muestra todos juntos y no ejecuta la simulación (se pueden probar con `error-tamano.csv` y `error-varios.csv`).

## Cómo se calculan los tiempos
- **TR** (tiempo de retorno) = fin − ingreso a la cola de Listos.
- **TE** (tiempo de espera) = TR − irrupción.
- **Rendimiento** = procesos terminados / tiempo total de simulación.

El tiempo se cuenta desde que el proceso entra a la cola de Listos, no desde que llega al sistema. Un proceso que espera en Listo/Suspendido por falta de memoria todavía no cuenta ese tiempo.

## Si Windows bloquea el programa
Los `.exe` no están firmados digitalmente, por lo que Windows puede mostrar avisos al ejecutarlos. No indica un virus: es esperable en software de uso académico.

- **SmartScreen ("Windows protegió su PC"):** aparece al ejecutar `SimuladorSetup.exe` y dice "Editor desconocido". Para continuar:
  1. Clic en **Más información**.
  2. Clic en **Ejecutar de todas formas**.
- **Control Inteligente de Aplicaciones (Windows 11):** en algunas PC puede bloquear el programa o el desinstalador (`unins000.exe`). Si pasa, se puede borrar a mano la carpeta `C:\Users\<usuario>\AppData\Local\Programs\SimuladorSO` y los accesos del menú Inicio y del escritorio.
- **Alternativa:** ejecutar desde el código fuente (ver abajo).

Probado en una PC con Windows 11 sin Python: la instalación (con el aviso de SmartScreen), la ventana, la consola y la desinstalación funcionaron.

## Desde el código fuente (para desarrollo)
Requiere Python 3.10 o superior.
```
python app.py
python main.py datos\procesos-ejemplo.csv
python -m unittest discover -s tests -v
```