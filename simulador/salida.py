"""RESPONSABLE: Miembro 7

Sólo arma TEXTO (no hace print): así se puede testear y después reemplazar por la interfaz gráfica.
"""
from simulador.estadisticas import Estadisticas
from simulador.motor import Instantanea


def _cola(procesos: list[dict]) -> str:
    """Formatea una cola como 'P1(4), P3(3)' (id y tiempo restante). Vacía -> '—'."""
    if not procesos:
        return '—'
    return ', '.join(f"P{p['id']}({p['restante']})" for p in procesos)


def render_instante(inst: Instantanea) -> str:
    """Pantalla de un instante: encabezado con t y eventos, estado de la CPU ("ociosa" si no hay),
    tabla de particiones (Id, Inicio, Tamaño, Proceso, Frag. interna), colas Listo y
    Listo/Suspendido, y procesos Nuevos esperando cupo."""
    # Encabezado con los eventos del instante
    eventos = []
    if inst.eventos.arribos:
        eventos.append('Llegó: ' + ', '.join(f'P{i}' for i in inst.eventos.arribos))
    if inst.eventos.terminados:
        eventos.append('Terminó: ' + ', '.join(f'P{i}' for i in inst.eventos.terminados))
    if inst.eventos.desalojado is not None:
        eventos.append(f'Desalojado: P{inst.eventos.desalojado}')
    encabezado = f't = {inst.t}'
    if eventos:
        encabezado += ' │ ' + ' │ '.join(eventos)

    lineas = [f'══════════ {encabezado} ══════════', '']

    # Estado de la CPU
    if inst.cpu is None:
        lineas.append('CPU: ociosa')
    else:
        lineas.append(f"CPU: P{inst.cpu['id']} (restante {inst.cpu['restante']})")
    lineas.append('')

    # Tabla de particiones
    lineas.append(f"{'Part':<5}│ {'Inicio':>6} │ {'Tamaño':>7} │ {'Proceso':<8}│ {'Frag.Int':>8}")
    lineas.append('─────┼────────┼─────────┼─────────┼─────────')

    # El SO ocupa desde la dirección 0 hasta donde empieza la primera partición de usuario
    if inst.particiones:
        tam_so = inst.particiones[0]['inicio']
        lineas.append(f"{'SO':<5}│ {0:>6} │ {str(tam_so) + 'K':>7} │ {'SO':<8}│ {'-':>8}")

    for part in inst.particiones:
        if part['proceso_id'] is None:
            proceso = 'libre'
        else:
            proceso = f"P{part['proceso_id']}"
        frag = '-' if part['frag_interna'] is None else f"{part['frag_interna']}K"
        lineas.append(
            f"{part['id']:<5}│ {part['inicio']:>6} │ {str(part['tamano']) + 'K':>7} │ "
            f"{proceso:<8}│ {frag:>8}"
        )
    lineas.append('')

    # Colas
    lineas.append(f'Listos: {_cola(inst.listos)}')
    lineas.append(f'Listos/Susp.: {_cola(inst.suspendidos)}')
    lineas.append(f'Esperando cupo: {_cola(inst.nuevos)}')

    return '\n'.join(lineas)


def render_informe(est: Estadisticas) -> str:
    """Informe final: tabla por proceso (Id, Arribo, Ingreso a Listos, Irrupción, Fin, TR, TE),
    promedios con 2 decimales y rendimiento."""
    lineas = ['══════════ INFORME FINAL ══════════', '']
    lineas.append(
        f"{'Id':>4} │ {'Arribo':>6} │ {'Ing.Listos':>10} │ {'Irrupción':>9} │ {'Fin':>4} │ {'TR':>4} │ {'TE':>4}"
    )
    lineas.append('─────┼────────┼────────────┼───────────┼──────┼──────┼──────')

    for f in est.por_proceso:
        lineas.append(
            f"{'P' + str(f['id']):>4} │ {f['arribo']:>6} │ {f['ingreso_listo']:>10} │ {f['irrupcion']:>9} │ "
            f"{f['fin']:>4} │ {f['tr']:>4} │ {f['te']:>4}"
        )

    lineas.append('')
    lineas.append('TR y TE se cuentan desde el ingreso a la cola de Listos.')
    lineas.append(f'Promedio TR: {est.promedio_tr:.2f}')
    lineas.append(f'Promedio TE: {est.promedio_te:.2f}')
    lineas.append(f'Rendimiento: {est.rendimiento:.2f} procesos por unidad de tiempo')

    return '\n'.join(lineas)
