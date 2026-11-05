"""RESPONSABLE: Miembro 7"""
from dataclasses import dataclass

from simulador.proceso import Proceso, Estado


@dataclass
class Estadisticas:
    por_proceso: list[dict]   # {id, arribo, ingreso_listo, irrupcion, fin, tr, te}
    promedio_tr: float
    promedio_te: float
    rendimiento: float        # procesos terminados / tiempo total (trabajos por unidad de tiempo)


def calcular_estadisticas(procesos: list[Proceso], tiempo_total: int) -> Estadisticas:
    """procesos: todos Terminados. tiempo_total: instante en que terminó el último."""
    terminados = [p for p in procesos if p.estado == Estado.TERMINADO]

    por_proceso = []
    suma_tr = 0
    suma_te = 0

    for p in terminados:
        por_proceso.append({
            "id": p.id,
            "arribo": p.arribo,
            "ingreso_listo": p.ingreso_listo,
            "irrupcion": p.irrupcion,
            "fin": p.fin,
            "tr": p.tiempo_retorno,
            "te": p.tiempo_espera,
        })
        suma_tr += p.tiempo_retorno
        suma_te += p.tiempo_espera

    n = len(terminados)
    promedio_tr = suma_tr / n if n > 0 else 0.0
    promedio_te = suma_te / n if n > 0 else 0.0
    rendimiento = n / tiempo_total if tiempo_total > 0 else 0.0

    return Estadisticas(
        por_proceso=por_proceso,
        promedio_tr=promedio_tr,
        promedio_te=promedio_te,
        rendimiento=rendimiento,
    )
