# HOWTO — Cómo instalar y usar el simulador

> Borrador: lo completa el Miembro 7 cuando el instalador esté probado.

## Instalación (no requiere Python ni internet)
1. Ejecutar `SimuladorSetup.exe`.
2. Siguiente → Siguiente → Instalar. No pide permisos de administrador.
3. Queda en el menú Inicio: **Simulador** (con ventana) y **Simulador en consola** (ejemplo y carga manual).

## Uso
**Con ventana** (`simulador.exe`): abre con el ejemplo cargado.
- **Siguiente evento** (o Enter) avanza hasta que llega o termina un proceso.
- **Abrir CSV** carga otro archivo y **Carga manual** permite escribir los procesos.
- **Reiniciar** vuelve a empezar con los mismos procesos.

**En consola** (`simulador-consola.exe`):
- **Con archivo**: `simulador-consola.exe ruta\al\archivo.csv`
- **Carga manual**: abrirlo sin parámetros y responder lo que pide.
- En cada evento la simulación se detiene: presionar **Enter** para continuar.

## Formato del archivo
```
id,tamano,arribo,irrupcion
1,200,0,5
2,150,1,2
```
Máximo 10 procesos. El tamaño se expresa en K y no puede superar 450.

## Desde el código fuente (para desarrollo)
Requiere Python 3.10 o superior.
```
python app.py
python main.py datos\procesos-ejemplo.csv
python -m unittest discover -s tests -v
```
