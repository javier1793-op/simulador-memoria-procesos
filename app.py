"""Punto de entrada de la versión con ventana:   python app.py [archivo.csv]

La versión de consola (main.py) sigue funcionando igual; las dos usan el mismo motor.
"""
import sys

from simulador.interfaz import ejecutar

if __name__ == '__main__':
    ejecutar(sys.argv[1] if len(sys.argv) > 1 else None)
