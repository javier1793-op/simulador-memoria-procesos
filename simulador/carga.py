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
    lineas = texto.splitlines()
    if not lineas:
        return []

    procesos = []
    header_saltado = False

    for num_linea, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if not linea:
            continue

        # Saltamos la primera línea no vacía (el encabezado)
        if not header_saltado:
            header_saltado = True
            continue

        partes = [p.strip() for p in linea.split(",")]
        if len(partes) != 4:
            raise ErrorCarga(
                f"Línea {num_linea}: la fila debe contener exactamente 4 columnas."
            )

        try:
            p_id = int(partes[0])
            tamano = int(partes[1])
            arribo = int(partes[2])
            irrupcion = int(partes[3])
        except ValueError:
            raise ErrorCarga(
                f"Línea {num_linea}: los valores deben ser números enteros."
            )

        procesos.append(
            {"id": p_id, "tamano": tamano, "arribo": arribo, "irrupcion": irrupcion}
        )

    return procesos


def validar_procesos(lista: list[dict]) -> list[str]:
    errores = []

    if not lista:
        errores.append("No se ingresaron procesos.")
        return errores

    if len(lista) > MAX_PROCESOS:
        errores.append(f"No se pueden cargar más de {MAX_PROCESOS} procesos.")

    ids_vistos = set()

    for proc in lista:
        p_id = proc.get("id")
        tamano = proc.get("tamano")
        arribo = proc.get("arribo")
        irrupcion = proc.get("irrupcion")

        # Validar ID
        if type(p_id) is not int or p_id <= 0:
            errores.append(f"El ID {p_id} debe ser un entero positivo.")
        elif p_id in ids_vistos:
            errores.append(f"El ID {p_id} está duplicado.")
        else:
            ids_vistos.add(p_id)

        # Validar tamaño
        if type(tamano) is not int:
            errores.append(f"Proceso {p_id}: el tamaño ({tamano}) debe ser un entero.")
        elif tamano < 1 or tamano > MEMORIA_USUARIO:
            errores.append(
                f"Proceso {p_id}: el tamaño ({tamano}) debe estar entre 1 y {MEMORIA_USUARIO}K."
            )

        # Validar arribo
        if type(arribo) is not int:
            errores.append(f"Proceso {p_id}: el tiempo de arribo ({arribo}) debe ser un entero.")
        elif arribo < 0:
            errores.append(
                f"Proceso {p_id}: el tiempo de arribo ({arribo}) debe ser mayor o igual a 0."
            )

        # Validar irrupción
        if type(irrupcion) is not int:
            errores.append(f"Proceso {p_id}: el tiempo de irrupción ({irrupcion}) debe ser un entero.")
        elif irrupcion < 1:
            errores.append(
                f"Proceso {p_id}: el tiempo de irrupción ({irrupcion}) debe ser mayor o igual a 1."
            )

    return errores


def cargar_archivo(ruta_archivo: str) -> list[Proceso]:
    """Lee, parsea, valida y devuelve Proceso[]."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        raise ErrorCarga(f"No se encontró el archivo: {ruta_archivo}")
    except Exception as e:
        raise ErrorCarga(f"Error al leer el archivo: {e}")

    filas = parsear_csv(contenido)
    errores = validar_procesos(filas)

    if errores:
        raise ErrorCarga("\n".join(errores))

    procesos = []
    for f in filas:
        procesos.append(
            Proceso(
                id=f["id"],
                tamano=f["tamano"],
                arribo=f["arribo"],
                irrupcion=f["irrupcion"],
            )
        )

    return procesos


def carga_manual(entrada=input) -> list[Proceso]:
    """Pide los datos por teclado (re-preguntando si un dato es inválido)."""
    print("\n--- Carga Manual de Procesos ---")

    while True:
        try:
            cant = int(entrada("¿Cuántos procesos desea cargar? (1 a 10): ").strip())
            if 1 <= cant <= MAX_PROCESOS:
                break
            print(f"Error: la cantidad debe estar entre 1 y {MAX_PROCESOS}.")
        except ValueError:
            print("Error: ingrese un número entero válido.")

    procesos = []

    for i in range(1, cant + 1):
        print(f"\n--- Proceso {i} de {cant} ---")

        # Pedir Tamaño
        while True:
            try:
                tamano = int(
                    entrada(f"  Tamaño en K (1 a {MEMORIA_USUARIO}): ").strip()
                )
                if 1 <= tamano <= MEMORIA_USUARIO:
                    break
                print(f"  Error: el tamaño debe estar entre 1 y {MEMORIA_USUARIO}K.")
            except ValueError:
                print("  Error: debe ingresar un entero.")

        # Pedir Arribo
        while True:
            try:
                arribo = int(entrada("  Tiempo de arribo (>= 0): ").strip())
                if arribo >= 0:
                    break
                print("  Error: el arribo debe ser mayor o igual a 0.")
            except ValueError:
                print("  Error: debe ingresar un entero.")

        # Pedir Irrupción
        while True:
            try:
                irrupcion = int(entrada("  Tiempo de irrupción (>= 1): ").strip())
                if irrupcion >= 1:
                    break
                print("  Error: la irrupción debe ser mayor o igual a 1.")
            except ValueError:
                print("  Error: debe ingresar un entero.")

        procesos.append(
            Proceso(id=i, tamano=tamano, arribo=arribo, irrupcion=irrupcion)
        )

    return procesos
