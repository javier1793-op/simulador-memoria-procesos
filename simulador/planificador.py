"""RESPONSABLE: Miembro 4

Planificador de corto plazo: SRTF (Shortest Remaining Time First), con apropiación.
Y el registro del diagrama de Gantt.
"""
from typing import NamedTuple

from simulador.proceso import Estado, Proceso


class ResultadoPlanificacion(NamedTuple):
    en_ejecucion: Proceso | None
    desalojado: Proceso | None    # el que perdió la CPU por apropiación (o None)


def clave_srtf(p: Proceso) -> tuple:
    """Clave de orden SRTF para sorted()/min(): menor restante;
    empate -> menor arribo; empate -> menor id."""
    raise NotImplementedError('TODO M4: clave_srtf')


def elegir_siguiente(procesos: list[Proceso]) -> Proceso | None:
    """Devuelve el Listo que debería ejecutar (sin modificar nada), o None si no hay Listos.
    `procesos` son TODOS los procesos: filtrar por estado Listo."""
    raise NotImplementedError('TODO M4: elegir_siguiente')


def planificar(procesos: list[Proceso]) -> ResultadoPlanificacion:
    """Aplica SRTF y cambia los estados que correspondan:
      - si no hay nadie en Ejecución y hay Listos: el elegido pasa a Ejecución
      - si hay alguien en Ejecución y un Listo tiene restante ESTRICTAMENTE menor:
          el que ejecutaba -> Listo (conserva su partición), el elegido -> Ejecución
    """
    raise NotImplementedError('TODO M4: planificar')


class Tramo(NamedTuple):
    desde: int
    hasta: int
    proceso_id: int | None   # None = CPU ociosa


class Gantt:
    """Qué proceso usó la CPU en cada tick, para mostrar el diagrama de Gantt al final
    (no lo pide la consigna, pero sirve muchísimo para explicar SRTF en el video)."""

    def __init__(self):
        self.ticks: list[int | None] = []   # ticks[t] = id que ejecutó en [t, t+1), None si ociosa

    def registrar(self, t: int, proceso_id: int | None) -> None:
        raise NotImplementedError('TODO M4: registrar')

    def tramos(self) -> list[Tramo]:
        """Agrupa ticks consecutivos del mismo proceso.
        Ej: ticks [1, 2, 2, None, 1] ->
            [Tramo(0, 1, 1), Tramo(1, 3, 2), Tramo(3, 4, None), Tramo(4, 5, 1)]"""
        raise NotImplementedError('TODO M4: tramos')

    def a_texto(self) -> str:
        """Texto tipo:  | P1 | P2 | P2 | -- | P1 |  con la escala de tiempos abajo."""
        raise NotImplementedError('TODO M4: a_texto')
