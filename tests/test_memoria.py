"""Miembro 3 — correr con:  python -m unittest tests.test_memoria -v"""
import unittest

from simulador.memoria import Memoria
from tests.ayuda import crear


def mapa(m):
    """Resumen de la memoria para comparar fácil: (inicio, tamano, proceso_id)."""
    return [(p.inicio, p.tamano, p.proceso_id) for p in m.particiones]


class TestMemoria(unittest.TestCase):
    def test_arranca_con_un_hueco_de_450(self):
        m = Memoria()
        self.assertEqual(mapa(m), [(100, 450, None)])
        self.assertEqual(m.memoria_libre_total(), 450)

    def test_asignar_parte_el_hueco(self):
        m = Memoria()
        p1 = crear(1, 200, 0, 5)
        self.assertTrue(m.asignar(p1))
        self.assertEqual(mapa(m), [(100, 200, 1), (300, 250, None)])
        self.assertIsNotNone(p1.particion_id)

    def test_tamano_justo_no_deja_hueco_de_cero(self):
        m = Memoria()
        m.asignar(crear(1, 450, 0, 1))
        self.assertEqual(mapa(m), [(100, 450, 1)])

    def test_sin_hueco_devuelve_false_y_no_toca_nada(self):
        m = Memoria()
        m.asignar(crear(1, 400, 0, 1))
        p2 = crear(2, 100, 0, 1)
        self.assertFalse(m.asignar(p2))
        self.assertIsNone(p2.particion_id)
        self.assertEqual(mapa(m), [(100, 400, 1), (500, 50, None)])

    def test_best_fit_elige_el_mas_chico_que_alcanza(self):
        m = Memoria()
        a, b, c, d = crear(1, 100, 0, 1), crear(2, 50, 0, 1), crear(3, 100, 0, 1), crear(4, 150, 0, 1)
        for p in (a, b, c, d):
            m.asignar(p)          # a 100-199, b 200-249, c 250-349, d 350-499, libre 500 (50K)
        m.liberar(a)              # hueco 100K en 100
        m.liberar(c)              # hueco 100K en 250
        m.asignar(crear(5, 40, 0, 1))   # First-Fit iría a 100; Best-Fit va al de 50K en 500
        self.assertEqual(next(p.inicio for p in m.particiones if p.proceso_id == 5), 500)

    def test_best_fit_empate_menor_direccion(self):
        m = Memoria()
        a, b, c = crear(1, 100, 0, 1), crear(2, 50, 0, 1), crear(3, 100, 0, 1)
        for p in (a, b, c):
            m.asignar(p)
        m.asignar(crear(4, 200, 0, 1))  # ocupa el resto
        m.liberar(a)
        m.liberar(c)                    # dos huecos de 100K: en 100 y en 250
        self.assertEqual(m.buscar_hueco_best_fit(80).inicio, 100)

    def test_liberar_fusiona_a_la_derecha(self):
        m = Memoria()
        p1 = crear(1, 200, 0, 5)
        m.asignar(p1)
        m.liberar(p1)
        self.assertEqual(mapa(m), [(100, 450, None)])
        self.assertIsNone(p1.particion_id)

    def test_liberar_fusiona_a_ambos_lados(self):
        m = Memoria()
        a, b, c = crear(1, 100, 0, 1), crear(2, 100, 0, 1), crear(3, 100, 0, 1)
        for p in (a, b, c):
            m.asignar(p)
        m.liberar(a)
        m.liberar(c)   # c se fusiona con el hueco del final
        self.assertEqual(mapa(m), [(100, 100, None), (200, 100, 2), (300, 250, None)])
        m.liberar(b)   # b queda entre dos huecos -> un solo hueco
        self.assertEqual(mapa(m), [(100, 450, None)])

    def test_tabla_frag_interna_cero_y_none_en_huecos(self):
        m = Memoria()
        p1 = crear(1, 200, 0, 5)
        m.asignar(p1)
        tabla = m.tabla_particiones({1: p1})
        self.assertEqual([(f['inicio'], f['tamano'], f['proceso_id'], f['frag_interna']) for f in tabla],
                         [(100, 200, 1, 0), (300, 250, None, None)])
        self.assertTrue(all(isinstance(f['id'], int) for f in tabla))


if __name__ == '__main__':
    unittest.main()
