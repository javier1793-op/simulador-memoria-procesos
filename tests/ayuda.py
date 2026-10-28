from simulador.proceso import Proceso


def crear(id, tamano, arribo, irrupcion, estado=None):
    """Crea un proceso y, si se pide, lo fuerza a un estado (sin validar transición: sólo para tests)."""
    p = Proceso(id, tamano, arribo, irrupcion)
    if estado is not None:
        p.estado = estado
    return p
