"""RESPONSABLE: Miembro 6 (integrador)

Punto de entrada:   python main.py [archivo.csv]
Sin archivo -> carga manual por teclado.
"""
import sys

from simulador.carga import ErrorCarga, carga_manual, cargar_archivo
from simulador.estadisticas import calcular_estadisticas
from simulador.motor import Eventos, Simulador
from simulador.salida import render_informe, render_instante


def main() -> int:
    try:
        procesos = cargar_archivo(sys.argv[1]) if len(sys.argv) > 1 else carga_manual()
    except (ErrorCarga, OSError) as e:
        print(f'Error: {e}')
        input('Presione Enter para salir...')
        return 1

    sim = Simulador(procesos)
    while not sim.finalizada:
        inst, hay_evento = sim.paso()
        if hay_evento:
            print(render_instante(inst))
            # La consigna prohíbe corridas ininterrumpidas: se frena en cada evento.
            input('Presione Enter para continuar...')

    # Estado final (el último proceso terminó en sim.t) + Gantt + informe
    print(render_instante(sim.instantanea(Eventos(terminados=sim.terminados_en_este_instante))))
    print(sim.gantt.a_texto())
    print(render_informe(calcular_estadisticas(procesos, sim.t)))
    input('Presione Enter para salir...')   # que la ventana del .exe no se cierre sola
    return 0


if __name__ == '__main__':
    sys.exit(main())
