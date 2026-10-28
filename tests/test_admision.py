"""Miembro 5 — correr con:  python -m unittest tests.test_admision -v

Usa la Memoria real: hasta que el Miembro 3 termine, estos tests fallan por eso (es esperable).
Mientras tanto se puede probar con una memoria falsa (un objeto con asignar() que devuelve True/False).
"""
import unittest

from simulador.admision import admitir_nuevos, contar_en_sistema, promover_suspendidos
from simulador.memoria import Memoria
from simulador.proceso import Estado
from tests.ayuda import crear

NUEVO, LISTO, SUSP, EJEC, TERM = (Estado.NUEVO, Estado.LISTO, Estado.LISTO_SUSPENDIDO,
                                  Estado.EJECUCION, Estado.TERMINADO)


def ids(lista):
    return [p.id for p in lista]


class TestAdmision(unittest.TestCase):
    def test_cuenta_ejec_listo_y_suspendido(self):
        procs = [crear(1, 1, 0, 1, EJEC), crear(2, 1, 0, 1, LISTO), crear(3, 1, 0, 1, SUSP),
                 crear(4, 1, 0, 1, NUEVO), crear(5, 1, 0, 1, TERM)]
        self.assertEqual(contar_en_sistema(procs), 3)

    def test_admite_a_listo_con_cupo_y_memoria(self):
        procs = [crear(1, 200, 0, 5)]
        r = admitir_nuevos(procs, Memoria(), 0)
        self.assertEqual(ids(r.admitidos), [1])
        self.assertEqual(procs[0].estado, LISTO)
        self.assertIsNotNone(procs[0].particion_id)

    def test_no_admite_los_que_no_llegaron(self):
        procs = [crear(1, 200, 5, 5)]
        admitir_nuevos(procs, Memoria(), 4)
        self.assertEqual(procs[0].estado, NUEVO)

    def test_sin_memoria_pasa_a_suspendido(self):
        procs = [crear(1, 400, 0, 5), crear(2, 100, 0, 5)]
        r = admitir_nuevos(procs, Memoria(), 0)
        self.assertEqual(ids(r.admitidos), [1])
        self.assertEqual(ids(r.suspendidos), [2])
        self.assertEqual(procs[1].estado, SUSP)
        self.assertIsNone(procs[1].particion_id)

    def test_grado_multiprogramacion_5(self):
        procs = [crear(i, 10, 0, 3) for i in range(1, 7)]
        r = admitir_nuevos(procs, Memoria(), 0)
        self.assertEqual(len(r.admitidos), 5)
        self.assertEqual(ids(r.en_espera), [6])
        self.assertEqual(procs[5].estado, NUEVO)

    def test_el_que_espero_entra_despues(self):
        # bug "arribo = t" del diagrama original: el que no entró no se tiene que perder
        m = Memoria()
        procs = [crear(i, 10, 0, 3) for i in range(1, 7)]
        admitir_nuevos(procs, m, 0)
        procs[0].estado = TERM
        m.liberar(procs[0])
        admitir_nuevos(procs, m, 3)   # t = 3, el proceso 6 llegó en t = 0
        self.assertEqual(procs[5].estado, LISTO)

    def test_orden_por_arribo_no_por_lista(self):
        procs = [crear(1, 300, 2, 1), crear(2, 300, 1, 1)]
        admitir_nuevos(procs, Memoria(), 2)
        self.assertEqual(procs[1].estado, LISTO)   # llegó antes, se queda con la memoria
        self.assertEqual(procs[0].estado, SUSP)

    def test_promueve_los_que_entran_saltando_los_que_no(self):
        m = Memoria()
        ocupa = crear(9, 300, 0, 1, LISTO)
        m.asignar(ocupa)                     # quedan 150K libres
        grande = crear(1, 200, 0, 1, SUSP)
        chico = crear(2, 100, 1, 1, SUSP)
        r = promover_suspendidos([ocupa, grande, chico], m)
        self.assertEqual(ids(r), [2])
        self.assertEqual(grande.estado, SUSP)
        self.assertEqual(chico.estado, LISTO)


if __name__ == '__main__':
    unittest.main()
