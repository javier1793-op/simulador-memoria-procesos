"""RESPONSABLE: Miembro 2

Contrato compartido: TODOS los módulos usan esta clase.
No cambiar nombres de campos sin avisar al grupo.
"""
from enum import Enum


class Estado(Enum):
    """Estados del ciclo de vida que pide la consigna (no hay Bloqueado)."""
    NUEVO = 'Nuevo'
    LISTO = 'Listo'
    LISTO_SUSPENDIDO = 'Listo/Suspendido'
    EJECUCION = 'Ejecución'
    TERMINADO = 'Terminado'


# Transiciones permitidas: estado actual -> estados a los que puede pasar.
TRANSICIONES = {
    Estado.NUEVO: {Estado.LISTO, Estado.LISTO_SUSPENDIDO},
    Estado.LISTO_SUSPENDIDO: {Estado.LISTO},
    Estado.LISTO: {Estado.EJECUCION},
    Estado.EJECUCION: {Estado.LISTO, Estado.TERMINADO},
    Estado.TERMINADO: set(),
}


class Proceso:
    """Funciona como el PCB (Process Control Block) del simulador."""

    def __init__(self, id: int, tamano: int, arribo: int, irrupcion: int):
        self.id = id
        self.tamano = tamano          # en K
        self.arribo = arribo          # instante en que llega al sistema
        self.irrupcion = irrupcion    # tiempo total de CPU que necesita
        self.restante = irrupcion     # lo que le falta ejecutar (SRTF ordena por esto)
        self.estado = Estado.NUEVO
        self.particion_id = None      # id de la partición asignada (None si no está en memoria)
        self.fin = None               # instante en que terminó

    def cambiar_estado(self, nuevo: Estado) -> None:
        """Cambia el estado del proceso."""
        if nuevo not in TRANSICIONES[self.estado]:
            raise ValueError(f'Proceso {self.id}: transición inválida {self.estado.value} -> {nuevo.value}')

        self.estado = nuevo

    @property
    def tiempo_retorno(self):
        """TR = fin - arribo. Devolver None si todavía no terminó."""
        if self.fin is None:
            return None
        return self.fin - self.arribo

    @property
    def tiempo_espera(self):
        """TE = TR - irrupcion. Devolver None si todavía no terminó."""
        tr = self.tiempo_retorno
        if tr is None:
            return None
        return tr - self.irrupcion

    def __repr__(self):
        return f'P{self.id}({self.estado.value}, restante={self.restante})'
