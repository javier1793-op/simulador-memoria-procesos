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
        return all(p.estado == Estado.TERMINADO for p in self.procesos)

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
        # lo que terminó al final del tick anterior se informa ahora, en el instante t
        terminados = self.terminados_en_este_instante
        self.terminados_en_este_instante = []

        # 1 y 2: primero los suspendidos (ya ocupan cupo y llegaron antes), después los nuevos
        promover_suspendidos(self.procesos, self.memoria)
        admitir_nuevos(self.procesos, self.memoria, self.t)
        # TR y TE se cuentan desde la PRIMERA entrada a Listos: volver por un desalojo no la cambia
        for p in self.procesos:
            if p.estado == Estado.LISTO and p.ingreso_listo is None:
                p.ingreso_listo = self.t
        arribos = [p.id for p in self.procesos if p.arribo == self.t]

        # 3: corto plazo
        plan = planificar(self.procesos)

        # 4: foto del instante, antes de ejecutar
        eventos = Eventos(arribos=arribos, terminados=terminados,
                          desalojado=plan.desalojado.id if plan.desalojado else None)
        inst = self.instantanea(eventos)

        # 5 y 6: ejecutar una unidad de tiempo
        en_cpu = plan.en_ejecucion
        self.gantt.registrar(self.t, en_cpu.id if en_cpu else None)
        if en_cpu:
            en_cpu.restante -= 1
            if en_cpu.restante == 0:
                en_cpu.cambiar_estado(Estado.TERMINADO)
                en_cpu.fin = self.t + 1
                self.memoria.liberar(en_cpu)
                self.terminados_en_este_instante.append(en_cpu.id)

        # 7: avanza el reloj
        self.t += 1
        return inst, bool(arribos or terminados)

    def instantanea(self, eventos: Eventos) -> Instantanea:
        """Arma la Instantanea con el estado actual (usar memoria.tabla_particiones)."""
        def resumen(p: Proceso) -> dict:
            return {'id': p.id, 'tamano': p.tamano, 'arribo': p.arribo, 'restante': p.restante}

        def en_estado(estado: Estado, ordenar=lambda p: (p.arribo, p.id)) -> list[dict]:
            return [resumen(p) for p in sorted((p for p in self.procesos if p.estado == estado), key=ordenar)]

        en_cpu = next((p for p in self.procesos if p.estado == Estado.EJECUCION), None)
        return Instantanea(
            t=self.t,
            cpu={'id': en_cpu.id, 'restante': en_cpu.restante} if en_cpu else None,
            listos=en_estado(Estado.LISTO, ordenar=lambda p: (p.restante, p.arribo, p.id)),
            suspendidos=en_estado(Estado.LISTO_SUSPENDIDO),
            nuevos=[resumen(p) for p in self.procesos if p.estado == Estado.NUEVO and p.arribo <= self.t],
            terminados=[p.id for p in self.procesos if p.estado == Estado.TERMINADO],
            particiones=self.memoria.tabla_particiones({p.id: p for p in self.procesos}),
            eventos=eventos,
        )
