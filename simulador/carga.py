"""RESPONSABLE: Miembro 1

Entrada del simulador: leer procesos desde un CSV o por teclado, y validarlos.

Formato del CSV (con encabezado):
    id,tamano,arribo,irrupcion
    1,200,0,5
"""
from simulador.config import MAX_PROCESOS, MEMORIA_USUARIO
from simulador.proceso import Proceso


class ErrorCarga(ValueError):
    """Error en los datos de entrada (se le muestra al usuario tal cual)."""


def parsear_csv(texto: str) -> list[dict]:
    """Convierte el texto de un CSV en una lista de dicts {id, tamano, arribo, irrupcion}.

    - La primera línea es el encabezado y se saltea.
    - Ignorar líneas vacías y espacios alrededor de cada valor.
    - Convertir cada valor a int.
    - Si una línea no tiene 4 columnas o un valor no es un número entero,
      lanzar ErrorCarga indicando el NÚMERO DE LÍNEA.
    """
    raise NotImplementedError('TODO M1: parsear_csv')


def validar_procesos(lista: list[dict]) -> list[str]:
    """Valida los datos ANTES de simular. Devuelve la lista de errores (vacía = todo ok).

    Reglas:
      - entre 1 y MAX_PROCESOS procesos
      - id positivo y no repetido
      - tamano entre 1 y MEMORIA_USUARIO (uno más grande nunca entraría y la simulación no terminaría)
      - arribo >= 0
      - irrupcion >= 1
    No corta en el primer error: junta TODOS para mostrarle al usuario qué corregir.
    """
    raise NotImplementedError('TODO M1: validar_procesos')


def cargar_archivo(ruta: str) -> list[Proceso]:
    """Lee el archivo (encoding utf-8), lo parsea, lo valida y devuelve objetos Proceso.

    Si hay errores de validación, lanzar ErrorCarga con todos los mensajes (uno por línea).
    """
    raise NotImplementedError('TODO M1: cargar_archivo')


def carga_manual(entrada=input) -> list[Proceso]:
    """Pide por teclado la cantidad de procesos y, para cada uno, EN ESTE ORDEN: tamaño, arribo
    e irrupción (el id se asigna automático 1..n). Si un dato es inválido, se vuelve a preguntar
    ESE dato (ej: tamaño 999 o "abc" -> se pide el tamaño de nuevo).

    `entrada` es la función que lee del teclado (por defecto input); en los tests se reemplaza.
    Opcional: al final ofrecer guardar lo cargado como CSV en datos/.
    """
    raise NotImplementedError('TODO M1: carga_manual')
