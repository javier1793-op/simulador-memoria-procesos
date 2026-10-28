"""RESPONSABLE: Miembro 3

Memoria con particiones variables (MVT) y política Best-Fit.
"""
from dataclasses import dataclass

from simulador.config import MEMORIA_SO, MEMORIA_USUARIO, INICIO_USUARIO


@dataclass
class Particion:
    id: int
    inicio: int               # dirección de comienzo (K)
    tamano: int               # (K)
    proceso_id: int | None    # None = hueco libre


class Memoria:
    def __init__(self):
        self.tamano_so = MEMORIA_SO
        # siempre ordenadas por dirección de inicio
        self.particiones: list[Particion] = [Particion(1, INICIO_USUARIO, MEMORIA_USUARIO, None)]
        self.siguiente_id = 2

    def buscar_hueco_best_fit(self, tamano: int) -> Particion | None:
        """Best-Fit: el hueco libre MÁS CHICO cuyo tamaño sea >= tamano.
        Empate: el de menor dirección. Si no hay ninguno, None."""
        raise NotImplementedError('TODO M3: buscar_hueco_best_fit')

    def asignar(self, proceso) -> bool:
        """Intenta ubicar al proceso. Si hay hueco:
          - crea una partición del tamaño EXACTO del proceso al comienzo del hueco
          - lo que sobra queda como hueco libre a continuación (si sobra > 0)
          - setea proceso.particion_id
        Devuelve True si lo pudo ubicar, False si no (y no modifica nada)."""
        raise NotImplementedError('TODO M3: asignar')

    def liberar(self, proceso) -> None:
        """Libera la partición del proceso, la marca como hueco y la FUSIONA con los huecos
        libres contiguos (anterior y/o siguiente). Deja proceso.particion_id = None."""
        raise NotImplementedError('TODO M3: liberar')

    def tabla_particiones(self, procesos_por_id: dict | None = None) -> list[dict]:
        """Tabla para mostrar (sólo área de usuario, ordenada por inicio).
        Cada fila: {id, inicio, tamano, proceso_id, frag_interna}
        frag_interna = tamaño partición - tamaño proceso (en MVT siempre 0); en huecos libres None.
        procesos_por_id: {id: Proceso} para buscar el tamaño del proceso."""
        raise NotImplementedError('TODO M3: tabla_particiones')

    def memoria_libre_total(self) -> int:
        """Suma de todos los huecos libres (sirve para mostrar fragmentación externa)."""
        raise NotImplementedError('TODO M3: memoria_libre_total')
