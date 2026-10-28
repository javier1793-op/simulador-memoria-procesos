# Simulador de Asignación de Memoria y Planificación de Procesos

TPI de Sistemas Operativos — UTN FRRe — 2026

- **Memoria:** particiones variables (MVT), 100K para el SO + 450K para usuarios, política **Best-Fit**
- **CPU:** un solo procesador, **SRTF** (apropiativo)
- **Grado de multiprogramación:** máximo 5 (Ejecución + Listo + Listo/Suspendido)
- **Estados:** Nuevo, Listo, Listo/Suspendido, Ejecución, Terminado
- **Lenguaje:** Python 3.10 o superior, **sin librerías externas**
- **Entrega:** instalador `SimuladorSetup.exe` que funciona sin Python y sin internet

## Cómo ejecutarlo (desarrollo)

```bash
python main.py datos/procesos-ejemplo.csv
```

```bash
python -m unittest discover -s tests -v
```

Sin archivo (`python main.py`), se cargan los procesos a mano por teclado.

## Estructura

```
main.py                     entrada por consola                          (M6)
simulador/
  config.py                 parámetros de la consigna (no hardcodear números)
  carga.py                  leer CSV, validar, carga manual               (M1)
  proceso.py                clase Proceso (PCB) y estados                 (M2)
  memoria.py                MVT + Best-Fit                                (M3)
  planificador.py           SRTF + diagrama de Gantt                      (M4)
  admision.py               largo y mediano plazo, límite de 5            (M5)
  motor.py                  reloj y ciclo de simulación                   (M6)
  estadisticas.py, salida.py  informe y pantallas                         (M7)
tests/                      un archivo de tests por módulo
datos/                      archivos CSV de prueba
instalador/                 construir.bat + script de Inno Setup          (M7)
HOWTO.md                    instrucciones para el profe
docs/
  TAREAS-TRELLO.md          tareas por miembro y sprints
  diagrama-corregido.md     errores del diagrama original + versión corregida
  modulos/                  guía de cada módulo: qué es, por qué y cómo exponerlo
```

## Cómo trabajamos

0. Cada tarea se hace en una rama propia (`m3/memoria`) y entra a `main` sólo por Pull Request aprobado. Paso a paso en [docs/GUIA-GIT.md](docs/GUIA-GIT.md).
1. Cada miembro programa **sólo el archivo de su módulo**, donde dice `TODO Mx`.
2. Su módulo está terminado cuando pasan sus tests, por ejemplo: `python -m unittest tests.test_memoria -v`.
3. **No cambiar los nombres de funciones ni de campos** (son el contrato entre módulos). Si hace falta cambiarlos, se avisa en el grupo.
4. Al terminar, completar la sección "Cómo lo implementé" de su guía en `docs/modulos/`.
