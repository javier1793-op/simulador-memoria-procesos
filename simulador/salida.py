"""RESPONSABLE: Miembro 7

Sólo arma TEXTO (no hace print): así se puede testear y después reemplazar por la interfaz gráfica.
"""
from simulador.estadisticas import Estadisticas
from simulador.motor import Instantanea


def render_instante(inst: Instantanea) -> str:
    """Pantalla de un instante: encabezado con t y eventos, estado de la CPU ("ociosa" si no hay),
    tabla de particiones (Id, Inicio, Tamaño, Proceso, Frag. interna), colas Listo y
    Listo/Suspendido, y procesos Nuevos esperando cupo."""
    raise NotImplementedError('TODO M7: render_instante')


def render_informe(est: Estadisticas) -> str:
    """Informe final: tabla por proceso (Id, Arribo, Irrupción, Fin, TR, TE),
    promedios con 2 decimales y rendimiento."""
    raise NotImplementedError('TODO M7: render_informe')
