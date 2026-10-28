"""RESPONSABLE: Miembro 5

Planificador de largo plazo (admisión de Nuevos) y de mediano plazo (Listo/Suspendido -> Listo).
"""
from typing import NamedTuple

from simulador.config import GRADO_MULTIPROGRAMACION
from simulador.proceso import Estado, Proceso


class ResultadoAdmision(NamedTuple):
    admitidos: list[Proceso]     # pasaron a Listo
    suspendidos: list[Proceso]   # pasaron a Listo/Suspendido
    en_espera: list[Proceso]     # se quedaron en Nuevo por falta de cupo


def contar_en_sistema(procesos: list[Proceso]) -> int:
    """Ejecución + Listo + Listo/Suspendido (lo que limita el grado de multiprogramación)."""
    raise NotImplementedError('TODO M5: contar_en_sistema')


def promover_suspendidos(procesos: list[Proceso], memoria) -> list[Proceso]:
    """Recorre los Listo/Suspendidos por orden de arribo (empate: id) y sube a memoria
    TODOS los que entren con Best-Fit (si uno no entra, se sigue con el siguiente).
    Devuelve los que pasaron a Listo."""
    raise NotImplementedError('TODO M5: promover_suspendidos')


def admitir_nuevos(procesos: list[Proceso], memoria, t: int) -> ResultadoAdmision:
    """Recorre los Nuevos con arribo <= t, por orden de arribo (empate: id). Para cada uno:
      - si contar_en_sistema(...) >= GRADO_MULTIPROGRAMACION: se queda en Nuevo
        (se reintenta en el próximo tick)
      - si entra en memoria (memoria.asignar): pasa a Listo
      - si no entra: pasa a Listo/Suspendido (igual ocupa cupo)
    """
    raise NotImplementedError('TODO M5: admitir_nuevos')
