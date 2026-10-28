"""RESPONSABLE: Miembro 6 (integrador)

Motor de la simulación: maneja el reloj y llama a los demás módulos en el orden correcto.
No imprime nada: devuelve Instantaneas que el módulo de salida (M7) convierte en texto.
"""
from dataclasses import dataclass, field

from simulador.admision import admitir_nuevos, promover_suspendidos
from simulador.memoria import Memoria
from simulador.planificador import Gantt, planificar
from simulador.proceso import Estado, Proceso


@dataclass
class Eventos:
    arribos: list[int] = field(default_factory=list)      # ids que llegaron en el instante t
    terminados: list[int] = field(default_factory=list)   # ids que terminaron en el instante t
    desalojado: int | None = None                         # id que perdió la CPU por SRTF


@dataclass
class Instantanea:
    """Foto del sistema en el instante t (contrato con el módulo de salida, M7).
    Las listas de procesos son dicts {id, tamano, arribo, restante}."""
    t: int
    cpu: dict | None                 # {id, restante} o None si está ociosa
    listos: list[dict]
    suspendidos: list[dict]
    nuevos: list[dict]               # ya arribados que esperan cupo
    terminados: list[int]
    particiones: list[dict]          # memoria.tabla_particiones(...)
    eventos: Eventos


class Simulador:
    def __init__(self, procesos: list[Proceso]):
        self.procesos = procesos
        self.memoria = Memoria()
        self.gantt = Gantt()
        self.t = 0
        self.terminados_en_este_instante: list[int] = []   # se reportan en el ciclo siguiente

    @property
    def finalizada(self) -> bool:
        """True cuando todos los procesos están Terminados."""
        raise NotImplementedError('TODO M6: finalizada')

    def paso(self) -> tuple[Instantanea, bool]:
        """Ejecuta UN ciclo completo en el instante self.t (ver docs/diagrama-corregido.md):
          1. promover_suspendidos
          2. admitir_nuevos (los que tengan arribo == t son los "arribos" del instante)
          3. planificar (SRTF)
          4. armar la Instantanea del instante t (ANTES de ejecutar)
          5. ejecutar 1 unidad al que está en Ejecución (restante -= 1) y registrar en el Gantt
             (None si la CPU está ociosa)
          6. si restante llegó a 0: Terminado, fin = t + 1, memoria.liberar
          7. t += 1
        Devuelve (instantanea, hay_evento).
        hay_evento = en este instante llegó algún proceso o terminó alguno."""
        raise NotImplementedError('TODO M6: paso')

    def instantanea(self, eventos: Eventos) -> Instantanea:
        """Arma la Instantanea con el estado actual (usar memoria.tabla_particiones)."""
        raise NotImplementedError('TODO M6: instantanea')
