# Tareas para Trello — Simulador de Memoria y Procesos

**Entrega final: 17/11.** Quedan unas 3 semanas, así que los sprints son cortos.

## Listas sugeridas en el tablero

`Backlog` · `Sprint actual` · `En progreso` · `En revisión` · `Hecho`

Etiquetas: `M1`…`M7` (por miembro), `código`, `tests`, `docs`, `video`, `bloqueante`.

## Tarjeta 0 — Preparar el entorno (todos, el primer día)

- [ ] Instalar **Python 3.12** desde python.org (marcar **"Add python.exe to PATH"** en el instalador)
- [ ] Instalar VS Code con la extensión **Python**
- [ ] Instalar Git, aceptar la invitación al repo y clonarlo (`docs/GUIA-GIT.md`, sección 2)
- [ ] Crear la rama de la primera tarea, por ejemplo `m3/memoria` (`docs/GUIA-GIT.md`, sección 3)
- [ ] Correr `python -m unittest discover -s tests -v`: tiene que ejecutar los tests (fallan porque falta el código; eso está bien)

## Regla de "Hecho" (vale para todas las tarjetas de código)

1. Pasan los tests de tu módulo: `python -m unittest tests.test_<tu_modulo> -v`
2. No cambiaste el **contrato** (nombres de funciones y campos) sin avisar en el grupo.
3. Completaste la sección "Cómo lo implementé" de tu guía en `docs/modulos/`.
4. Otra persona del grupo lo revisó (pasa por "En revisión").

## Orden de dependencias

```
M2 Proceso ──┬──> M4 SRTF ───────┐
             ├──> M5 Admisión ◄── M3 Memoria
             └──> M1 Carga        │
                                  ▼
                        M6 Motor (integra todo) ──> M7 Salida/Estadísticas
```

M2 y M3 son las bases: si alguien se traba, se le da prioridad a esos dos. **M2 tiene que terminar la clase `Proceso` en los primeros 2 días.** El resto puede avanzar en paralelo usando los tests, que no necesitan que los otros módulos estén listos (salvo M5, que usa la memoria de M3, y M6, que integra todo).

---

## Sprint 1 — Módulos en paralelo (27/10 → 03/11)

### 🟦 M1 — Carga y validación de procesos
**Archivo:** `simulador/carga.py` · **Tests:** `tests/test_carga.py` · **Guía:** `docs/modulos/01-carga.md`
- [ ] `parsear_csv`: lee el CSV con encabezado; ignora líneas vacías y espacios; soporta `\r\n`
- [ ] Error con número de línea si una fila está mal
- [ ] `validar_procesos`: máx. 10, ids únicos, tamaño 1..450, arribo ≥ 0, irrupción ≥ 1, enteros; junta TODOS los errores
- [ ] `cargar_archivo`: lee, parsea, valida y devuelve `Proceso[]`
- [ ] `carga_manual`: pedir los datos por teclado (re-preguntar si un dato es inválido)
- [ ] Opcional: guardar la carga manual como CSV
- [ ] Crear 2 archivos de prueba con errores en `datos/` para la demo

### 🟩 M2 — Modelo de Proceso, estados y casos de prueba
**Archivo:** `simulador/proceso.py` · **Tests:** `tests/test_proceso.py` · **Guía:** `docs/modulos/02-proceso.md`
- [ ] **(Día 1-2, bloqueante)** Validar transiciones en `cambiar_estado` (Nuevo → Ejecución tiene que fallar)
- [ ] Propiedades `tiempo_retorno` y `tiempo_espera`
- [ ] Diagrama de estados del proceso (para el video)
- [ ] Diseñar **3 casos de prueba** en `datos/` y resolverlos **a mano** (Gantt + tabla de memoria por evento + TR/TE): uno con fragmentación externa, uno con el límite de 5 procesos y uno con CPU ociosa
- [ ] Pasar esos 3 casos a `tests/test_integracion.py` (junto con M6)

### 🟨 M3 — Memoria MVT con Best-Fit
**Archivo:** `simulador/memoria.py` · **Tests:** `tests/test_memoria.py` · **Guía:** `docs/modulos/03-memoria.md`
- [ ] `buscar_hueco_best_fit` (hueco más chico que alcance; si empatan, el de menor dirección)
- [ ] `asignar`: partir el hueco en partición exacta + resto libre
- [ ] `liberar`: marcar libre y **fusionar** con los huecos contiguos
- [ ] `tabla_particiones` con fragmentación interna
- [ ] `memoria_libre_total`
- [ ] Dibujo de la memoria antes y después de asignar y de liberar (para el video)

### 🟧 M4 — Planificador SRTF y diagrama de Gantt
**Archivo:** `simulador/planificador.py` · **Tests:** `tests/test_planificador.py` · **Guía:** `docs/modulos/04-srtf.md`
- [ ] `clave_srtf` con desempates (arribo, id)
- [ ] `elegir_siguiente` (sólo Listos; None si no hay)
- [ ] `planificar`: asignar CPU libre y apropiación **estricta**
- [ ] `Gantt.registrar`, `tramos`, `a_texto`
- [ ] Ejemplo de SRTF vs SJF en una filmina (por qué SRTF es apropiativo)

### 🟥 M5 — Admisión: largo y mediano plazo
**Archivo:** `simulador/admision.py` · **Tests:** `tests/test_admision.py` · **Guía:** `docs/modulos/05-admision.md`
- [ ] `contar_en_sistema` (Ejec + Listo + Listo/Susp)
- [ ] `admitir_nuevos`: `arribo <= t`, por orden de arribo; respeta el límite de 5; Listo o Listo/Susp según la memoria
- [ ] `promover_suspendidos`: por orden de arribo, sin bloquearse si uno no entra
- [ ] Mientras M3 no termine, probar con una memoria "falsa" (un objeto con `asignar` que devuelve true/false)
- [ ] Explicación de los 3 planificadores (largo, mediano y corto plazo) para el video

### 🟪 M6 — Motor de simulación e integración *(sugerido: líder)*
**Archivos:** `simulador/motor.py`, `main.py` · **Tests:** `tests/test_integracion.py` · **Guía:** `docs/modulos/06-simulador.md`
- [ ] `finalizada`, `paso`, `instantanea` respetando el **orden del ciclo** del diagrama corregido
- [ ] Detectar eventos (arribo / terminación) → `hay_evento`
- [ ] Pausa con Enter en cada evento (consigna: nada de corridas ininterrumpidas)
- [ ] Integrar los módulos a medida que se terminan; correr todos los tests: `python -m unittest discover -s tests -v`
- [ ] Mantener actualizado `docs/diagrama-corregido.md`

### ⬜ M7 — Salida, estadísticas y entrega
**Archivos:** `simulador/salida.py`, `simulador/estadisticas.py`, `instalador/` · **Tests:** `tests/test_salida.py` · **Guía:** `docs/modulos/07-salida.md`
- [ ] `calcular_estadisticas`: TR, TE, promedios y rendimiento
- [ ] `render_instante`: CPU, tabla de particiones, colas y nuevos en espera (tablas alineadas)
- [ ] `render_informe`: tabla final con 2 decimales
- [ ] Generar `simulador.exe` con **PyInstaller** y el instalador `SimuladorSetup.exe` con **Inno Setup** (`instalador/construir.bat`)
- [ ] Probar el instalador en una PC **sin Python** y sin internet
- [ ] Completar `HOWTO.md` (lo pide la entrega)

---

## Sprint 2 — Integración y pruebas (03/11 → 10/11)

| Tarjeta | Responsable |
|---|---|
| Integrar todos los módulos y que todos los tests den 0 fallas | M6 |
| Correr los 3 casos a mano de M2 en el simulador y comparar | M2 + M6 |
| Pruebas "rompiendo" el programa: archivos mal formados, 10 procesos, procesos de 450K | M1 + M5 |
| Revisión cruzada de código: cada uno revisa el módulo del siguiente (M1→M2, …, M7→M1) | Todos |
| Instalador + HOWTO probado en una PC sin Python | M7 |
| (Opcional) Interfaz gráfica con los estilos: Tkinter o pywebview | A definir |

## Sprint 3 — Video y entrega (10/11 → 17/11)

| Tarjeta | Responsable |
|---|---|
| Guion del video (cada miembro explica su módulo, 1-2 min) | Líder |
| Grabar la demo con `datos/procesos-ejemplo.csv` | M6 |
| Cada uno graba su parte siguiendo la sección "Para exponer" de su guía | Todos |
| Armar el paquete: SimuladorSetup.exe + código fuente + HOWTO → campus | M7 + Líder |
| Compartir el tablero de Trello con los docentes | Líder |
