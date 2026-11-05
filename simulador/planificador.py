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
    return (p.restante, p.arribo, p.id)


def elegir_siguiente(procesos: list[Proceso]) -> Proceso | None:
    """Devuelve el Listo que debería ejecutar (sin modificar nada), o None si no hay Listos.
    `procesos` son TODOS los procesos: filtrar por estado Listo."""
    listos = [p for p in procesos if p.estado == Estado.LISTO]
    if not listos:
        return None
    return min(listos, key=clave_srtf)


def planificar(procesos: list[Proceso]) -> ResultadoPlanificacion:
    """Aplica SRTF y cambia los estados que correspondan:
      - si no hay nadie en Ejecución y hay Listos: el elegido pasa a Ejecución
      - si hay alguien en Ejecución y un Listo tiene restante ESTRICTAMENTE menor:
          el que ejecutaba -> Listo (conserva su partición), el elegido -> Ejecución
    """
    en_ejecucion_actual = next((p for p in procesos if p.estado == Estado.EJECUCION), None)
    siguiente = elegir_siguiente(procesos)

    if en_ejecucion_actual is None:
        if siguiente is not None:
            siguiente.cambiar_estado(Estado.EJECUCION)
            return ResultadoPlanificacion(en_ejecucion=siguiente, desalojado=None)
        return ResultadoPlanificacion(en_ejecucion=None, desalojado=None)
    else:
        # Verificar apropiación estricta
        if siguiente is not None and siguiente.restante < en_ejecucion_actual.restante:
            en_ejecucion_actual.cambiar_estado(Estado.LISTO)
            siguiente.cambiar_estado(Estado.EJECUCION)
            return ResultadoPlanificacion(en_ejecucion=siguiente, desalojado=en_ejecucion_actual)
        else:
            return ResultadoPlanificacion(en_ejecucion=en_ejecucion_actual, desalojado=None)


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
        while len(self.ticks) < t:
            self.ticks.append(None)
        self.ticks.append(proceso_id)

    def tramos(self) -> list[Tramo]:
        """Agrupa ticks consecutivos del mismo proceso.
        Ej: ticks [1, 2, 2, None, 1] ->
            [Tramo(0, 1, 1), Tramo(1, 3, 2), Tramo(3, 4, None), Tramo(4, 5, 1)]"""
        if not self.ticks:
            return []

        resultado = []
        inicio = 0
        actual = self.ticks[0]

        for i in range(1, len(self.ticks)):
            if self.ticks[i] != actual:
                resultado.append(Tramo(desde=inicio, hasta=i, proceso_id=actual))
                inicio = i
                actual = self.ticks[i]

        resultado.append(Tramo(desde=inicio, hasta=len(self.ticks), proceso_id=actual))
        return resultado

    def a_texto(self) -> str:
        """Texto tipo:  | P1 | P2 | P2 | -- | P1 |  con la escala de tiempos abajo."""
        tramos_lista = self.tramos()
        if not tramos_lista:
            return ""

        fila_bloques = "|"
        fila_tiempos = "0"
        for tramo in tramos_lista:
            nombre = f"P{tramo.proceso_id}" if tramo.proceso_id is not None else "--"
            fila_bloques += f" {nombre} |"
            # cada tiempo queda justo debajo de la barra donde termina su tramo
            fila_tiempos += str(tramo.hasta).rjust(len(fila_bloques) - len(fila_tiempos))

        return f"{fila_bloques}\n{fila_tiempos}"
