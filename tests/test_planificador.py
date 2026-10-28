"""Miembro 4 — correr con:  python -m unittest tests.test_planificador -v"""
import unittest

from simulador.planificador import Gantt, Tramo, clave_srtf, elegir_siguiente, planificar
from simulador.proceso import Estado
from tests.ayuda import crear

LISTO, EJEC, SUSP = Estado.LISTO, Estado.EJECUCION, Estado.LISTO_SUSPENDIDO


class TestSRTF(unittest.TestCase):
    def test_sin_listos_cpu_ociosa(self):
        self.assertIsNone(elegir_siguiente([crear(1, 10, 0, 3, SUSP)]))
        self.assertEqual(planificar([]), (None, None))

    def test_elige_menor_restante_ignorando_suspendidos(self):
        procs = [crear(1, 10, 0, 5, LISTO), crear(2, 10, 0, 2, LISTO), crear(3, 10, 0, 1, SUSP)]
        self.assertEqual(elegir_siguiente(procs).id, 2)

    def test_desempates_arribo_y_id(self):
        a, b, c = crear(5, 10, 3, 2), crear(4, 10, 1, 2), crear(2, 10, 1, 2)
        self.assertEqual([p.id for p in sorted([a, b, c], key=clave_srtf)], [2, 4, 5])

    def test_cpu_libre_el_elegido_ejecuta(self):
        procs = [crear(1, 10, 0, 5, LISTO), crear(2, 10, 0, 2, LISTO)]
        r = planificar(procs)
        self.assertEqual(r.en_ejecucion.id, 2)
        self.assertIsNone(r.desalojado)
        self.assertEqual(procs[1].estado, EJEC)
        self.assertEqual(procs[0].estado, LISTO)

    def test_apropiacion_estrictamente_menor(self):
        procs = [crear(1, 10, 0, 4, EJEC), crear(2, 10, 1, 2, LISTO)]
        r = planificar(procs)
        self.assertEqual(r.en_ejecucion.id, 2)
        self.assertEqual(r.desalojado.id, 1)
        self.assertEqual(procs[0].estado, LISTO)
        self.assertEqual(procs[1].estado, EJEC)

    def test_restante_igual_no_desaloja(self):
        procs = [crear(1, 10, 0, 2, EJEC), crear(2, 10, 1, 2, LISTO)]
        r = planificar(procs)
        self.assertEqual(r.en_ejecucion.id, 1)
        self.assertIsNone(r.desalojado)

    def test_desalojado_conserva_particion(self):
        p1 = crear(1, 10, 0, 4, EJEC)
        p1.particion_id = 7
        planificar([p1, crear(2, 10, 1, 1, LISTO)])
        self.assertEqual(p1.particion_id, 7)


class TestGantt(unittest.TestCase):
    def test_agrupa_ticks_consecutivos(self):
        g = Gantt()
        for t, pid in enumerate([1, 2, 2, None, 1]):
            g.registrar(t, pid)
        self.assertEqual(g.tramos(), [Tramo(0, 1, 1), Tramo(1, 3, 2), Tramo(3, 4, None), Tramo(4, 5, 1)])
        self.assertIsInstance(g.a_texto(), str)


if __name__ == '__main__':
    unittest.main()
