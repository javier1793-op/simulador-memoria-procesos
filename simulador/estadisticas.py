"""RESPONSABLE: Miembro 7"""
from dataclasses import dataclass

from simulador.proceso import Proceso


@dataclass
class Estadisticas:
    por_proceso: list[dict]   # {id, arribo, irrupcion, fin, tr, te}
    promedio_tr: float
    promedio_te: float
    rendimiento: float        # procesos terminados / tiempo total (trabajos por unidad de tiempo)


def calcular_estadisticas(procesos: list[Proceso], tiempo_total: int) -> Estadisticas:
    """procesos: todos Terminados. tiempo_total: instante en que terminó el último."""
    raise NotImplementedError('TODO M7: calcular_estadisticas')
