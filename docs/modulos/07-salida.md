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
Por proceso: TR y TE. Además, los promedios y el **rendimiento** (*throughput*) = procesos terminados / tiempo total.

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
(instalar Inno Setup 6 desde jrsoftware.org)
instalador\construir.bat      →  instalador\salida\SimuladorSetup.exe
```
**Importante:** probarlo en una PC que **no** tenga Python instalado antes de entregarlo. El antivirus a veces marca los `.exe` de PyInstaller: si pasa, hay que anotarlo en el HOWTO.

El HOWTO para el profe está en `HOWTO.md`, en la raíz del proyecto.

## Cómo lo implementé
> *(completar)*

## Para exponer (1-2 min)
1. Recorrer una pantalla de evento explicando cada parte.
2. Mostrar el informe final y explicar TR, TE y rendimiento con un proceso de ejemplo.
3. Mostrar la instalación con `SimuladorSetup.exe` en una PC sin Python.
