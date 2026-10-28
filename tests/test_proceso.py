"""Miembro 2 — correr con:  python -m unittest tests.test_proceso -v"""
import unittest

from simulador.proceso import Estado, Proceso


class TestProceso(unittest.TestCase):
    def nuevo(self, irrupcion=4):
        return Proceso(1, 100, 0, irrupcion)

    def test_nace_en_nuevo_sin_memoria(self):
        p = self.nuevo()
        self.assertEqual(p.estado, Estado.NUEVO)
        self.assertEqual(p.restante, 4)
        self.assertIsNone(p.particion_id)

    def test_transiciones_validas(self):
        p = self.nuevo()
        for e in (Estado.LISTO_SUSPENDIDO, Estado.LISTO, Estado.EJECUCION,
                  Estado.LISTO,  # apropiación SRTF
                  Estado.EJECUCION, Estado.TERMINADO):
            p.cambiar_estado(e)
        self.assertEqual(p.estado, Estado.TERMINADO)

    def test_nuevo_a_ejecucion_es_invalido(self):
        # era el error #6 del diagrama original
        with self.assertRaisesRegex(ValueError, 'inválida'):
            self.nuevo().cambiar_estado(Estado.EJECUCION)

    def test_suspendido_no_ejecuta_sin_pasar_por_listo(self):
        p = self.nuevo()
        p.cambiar_estado(Estado.LISTO_SUSPENDIDO)
        with self.assertRaises(ValueError):
            p.cambiar_estado(Estado.EJECUCION)

    def test_terminado_no_vuelve(self):
        p = self.nuevo(1)
        p.cambiar_estado(Estado.LISTO)
        p.cambiar_estado(Estado.EJECUCION)
        p.cambiar_estado(Estado.TERMINADO)
        with self.assertRaises(ValueError):
            p.cambiar_estado(Estado.LISTO)

    def test_tiempos_de_retorno_y_espera(self):
        p = Proceso(3, 300, 2, 3)
        self.assertIsNone(p.tiempo_retorno)
        self.assertIsNone(p.tiempo_espera)
        p.fin = 11
        self.assertEqual(p.tiempo_retorno, 9)
        self.assertEqual(p.tiempo_espera, 6)


if __name__ == '__main__':
    unittest.main()
