"""Miembro 7 — correr con:  python -m unittest tests.test_salida -v"""
import unittest

from simulador.estadisticas import calcular_estadisticas
from simulador.motor import Eventos, Instantanea
from simulador.proceso import Estado
from simulador.salida import render_informe, render_instante
from tests.ayuda import crear


def terminado(id, arribo, irrupcion, fin):
    p = crear(id, 10, arribo, irrupcion, Estado.TERMINADO)
    p.restante = 0
    p.fin = fin
    return p


def procesos_ejemplo():
    """Resultado de datos/procesos-ejemplo.csv calculado a mano (ver docs/modulos/06-simulador.md)."""
    return [terminado(1, 0, 5, 8), terminado(2, 1, 2, 3), terminado(3, 2, 3, 11), terminado(4, 3, 1, 4)]


class TestEstadisticas(unittest.TestCase):
    def test_tr_y_te_por_proceso(self):
        est = calcular_estadisticas(procesos_ejemplo(), 11)
        self.assertEqual([(f['id'], f['tr'], f['te']) for f in est.por_proceso],
                         [(1, 8, 3), (2, 2, 0), (3, 9, 6), (4, 1, 0)])

    def test_promedios_y_rendimiento(self):
        est = calcular_estadisticas(procesos_ejemplo(), 11)
        self.assertEqual(est.promedio_tr, 5)
        self.assertEqual(est.promedio_te, 2.25)
        self.assertAlmostEqual(est.rendimiento, 4 / 11)


class TestRender(unittest.TestCase):
    def test_informe_muestra_promedios(self):
        texto = render_informe(calcular_estadisticas(procesos_ejemplo(), 11))
        self.assertRegex(texto, r'5[.,]00')
        self.assertRegex(texto, r'2[.,]25')
        self.assertRegex(texto, r'0[.,]36')

    def test_pantalla_de_un_instante(self):
        texto = render_instante(Instantanea(
            t=2,
            cpu={'id': 2, 'restante': 1},
            listos=[{'id': 1, 'tamano': 200, 'arribo': 0, 'restante': 4}],
            suspendidos=[{'id': 3, 'tamano': 300, 'arribo': 2, 'restante': 3}],
            nuevos=[],
            terminados=[],
            particiones=[
                {'id': 1, 'inicio': 100, 'tamano': 200, 'proceso_id': 1, 'frag_interna': 0},
                {'id': 3, 'inicio': 300, 'tamano': 150, 'proceso_id': 2, 'frag_interna': 0},
                {'id': 4, 'inicio': 450, 'tamano': 100, 'proceso_id': None, 'frag_interna': None},
            ],
            eventos=Eventos(arribos=[3]),
        ))
        self.assertRegex(texto, r't\s*=\s*2')
        self.assertIn('450', texto)
        self.assertIn('3', texto)

    def test_cpu_ociosa(self):
        texto = render_instante(Instantanea(
            t=0, cpu=None, listos=[], suspendidos=[], nuevos=[], terminados=[],
            particiones=[{'id': 1, 'inicio': 100, 'tamano': 450, 'proceso_id': None, 'frag_interna': None}],
            eventos=Eventos(),
        ))
        self.assertRegex(texto.lower(), 'ocios')


if __name__ == '__main__':
    unittest.main()
