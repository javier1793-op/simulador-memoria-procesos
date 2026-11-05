"""Miembro 6 (+ Miembro 2 agrega más casos) — correr con:  python -m unittest tests.test_integracion -v

Simula datos/procesos-ejemplo.csv completo y compara con el resultado calculado a mano.
"""
import unittest

from simulador.motor import Simulador
from simulador.proceso import Estado
from tests.ayuda import crear


def ejemplo():
    return [crear(1, 200, 0, 5), crear(2, 150, 1, 2), crear(3, 300, 2, 3), crear(4, 50, 3, 1)]


def correr(procesos):
    sim = Simulador(procesos)
    instantes = []
    vueltas = 0
    while not sim.finalizada:
        vueltas += 1
        if vueltas > 1000:
            raise AssertionError('la simulación no termina')
        inst, hay_evento = sim.paso()
        if hay_evento:
            instantes.append(inst)
    return sim, instantes


class TestIntegracion(unittest.TestCase):
    def test_fin_de_cada_proceso_y_tiempo_total(self):
        procesos = ejemplo()
        sim, _ = correr(procesos)
        self.assertEqual([p.fin for p in procesos], [8, 3, 11, 4])
        self.assertEqual(sim.t, 11)
        self.assertTrue(all(p.estado == Estado.TERMINADO for p in procesos))

    def test_gantt(self):
        sim, _ = correr(ejemplo())
        self.assertEqual([tuple(x) for x in sim.gantt.tramos()],
                         [(0, 1, 1), (1, 3, 2), (3, 4, 4), (4, 8, 1), (8, 11, 3)])

    def test_se_muestra_en_arribos_y_terminaciones(self):
        _, instantes = correr(ejemplo())
        # arribos en 0,1,2,3 ; terminaciones en 3,4,8 ; el fin del último (11) lo muestra main.py
        self.assertEqual([i.t for i in instantes], [0, 1, 2, 3, 4, 8])

    def test_t2_proceso_3_suspendido_por_memoria(self):
        _, instantes = correr(ejemplo())
        t2 = next(i for i in instantes if i.t == 2)
        self.assertEqual(t2.cpu['id'], 2)
        self.assertEqual([p['id'] for p in t2.suspendidos], [3])
        self.assertEqual([(p['inicio'], p['tamano'], p['proceso_id']) for p in t2.particiones],
                         [(100, 200, 1), (300, 150, 2), (450, 100, None)])

    def test_t1_apropiacion(self):
        _, instantes = correr(ejemplo())
        t1 = next(i for i in instantes if i.t == 1)
        self.assertEqual(t1.cpu['id'], 2)
        self.assertEqual(t1.eventos.desalojado, 1)

    def test_tr_y_te_se_cuentan_desde_el_ingreso_a_listos(self):
        procesos = ejemplo()
        correr(procesos)
        # P3 llegó en t=2 pero estuvo Listo/Suspendido hasta t=8; ese tiempo no cuenta
        self.assertEqual([p.ingreso_listo for p in procesos], [0, 1, 8, 3])
        self.assertEqual([p.tiempo_retorno for p in procesos], [8, 2, 3, 1])
        self.assertEqual([p.tiempo_espera for p in procesos], [3, 0, 0, 0])

    def test_desalojado_conserva_su_primer_ingreso_a_listos(self):
        procesos = ejemplo()
        correr(procesos)
        # P1 volvió a Listos por apropiación en t=1, pero su referencia sigue siendo t=0
        self.assertEqual(procesos[0].ingreso_listo, 0)
        self.assertEqual(procesos[0].tiempo_espera, 3)

    def test_el_que_espero_cupo_cuenta_desde_que_entro_a_listos(self):
        procesos = [crear(i, 20, 0, 2) for i in range(1, 8)]
        correr(procesos)
        self.assertEqual([p.ingreso_listo for p in procesos], [0, 0, 0, 0, 0, 2, 4])
        self.assertEqual(procesos[6].tiempo_retorno, 10)
        self.assertEqual(procesos[6].tiempo_espera, 8)

    def test_cpu_ociosa_hasta_el_primer_arribo(self):
        procesos = [crear(1, 100, 3, 2)]
        sim, _ = correr(procesos)
        self.assertEqual(procesos[0].fin, 5)
        self.assertEqual([x.proceso_id for x in sim.gantt.tramos()], [None, 1])


if __name__ == '__main__':
    unittest.main()
