from typing import NamedTuple

from simulador.config import GRADO_MULTIPROGRAMACION
from simulador.proceso import Estado, Proceso


class ResultadoAdmision(NamedTuple):
    admitidos: list[Proceso]     # pasaron a Listo
    suspendidos: list[Proceso]   # pasaron a Listo/Suspendido
    en_espera: list[Proceso]     # se quedaron en Nuevo por falta de cupo


def contar_en_sistema(procesos: list[Proceso]) -> int:
    """Ejecución + Listo + Listo/Suspendido (lo que limita el grado de multiprogramación)."""
    estados_activos = {Estado.EJECUCION, Estado.LISTO, Estado.LISTO_SUSPENDIDO}
    return sum(1 for p in procesos if p.estado in estados_activos)


def promover_suspendidos(procesos: list[Proceso], memoria) -> list[Proceso]:
    """Recorre los Listo/Suspendidos por orden de arribo (empate: id) y sube a memoria
    TODOS los que entren con Best-Fit (si uno no entra, se sigue con el siguiente).
    Devuelve los que pasaron a Listo."""
    promovidos = []
    suspendidos = [p for p in procesos if p.estado == Estado.LISTO_SUSPENDIDO]
    suspendidos.sort(key=lambda p: (p.arribo, p.id))
    
    for p in suspendidos:
        if memoria.asignar(p):
            p.estado = Estado.LISTO
            promovidos.append(p)
        else:
            pass
            
    return promovidos


def admitir_nuevos(procesos: list[Proceso], memoria, t: int) -> ResultadoAdmision:
    """Recorre los Nuevos con arribo <= t, por orden de arribo (empate: id). Para cada uno:
      - si contar_en_sistema(...) >= GRADO_MULTIPROGRAMACION: se queda en Nuevo
        (se reintenta en el próximo tick)
      - si entra en memoria (memoria.asignar): pasa a Listo
      - si no entra: pasa a Listo/Suspendido (igual ocupa cupo)
    """
    admitidos = []
    suspendidos = []
    en_espera = []
    
    nuevos = [p for p in procesos if p.estado == Estado.NUEVO and p.arribo <= t]
    nuevos.sort(key=lambda p: (p.arribo, p.id))
    
    for p in nuevos:
        if contar_en_sistema(procesos) >= GRADO_MULTIPROGRAMACION:
            en_espera.append(p)
            continue 
            
        if memoria.asignar(p):
            p.estado = Estado.LISTO
            admitidos.append(p)
        else:
            p.estado = Estado.LISTO_SUSPENDIDO
            suspendidos.append(p)
            
    return ResultadoAdmision(admitidos, suspendidos, en_espera)