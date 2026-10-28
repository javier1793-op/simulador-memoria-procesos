"""Miembro 1 — correr con:  python -m unittest tests.test_carga -v"""
import unittest
from pathlib import Path

from simulador.carga import ErrorCarga, carga_manual, cargar_archivo, parsear_csv, validar_procesos
from simulador.proceso import Proceso

EJEMPLO = Path(__file__).resolve().parent.parent / 'datos' / 'procesos-ejemplo.csv'


def fila(id, tamano=100, arribo=0, irrupcion=1):
    return {'id': id, 'tamano': tamano, 'arribo': arribo, 'irrupcion': irrupcion}


class TestParsearCSV(unittest.TestCase):
    def test_encabezado_espacios_y_lineas_vacias(self):
        texto = 'id,tamano,arribo,irrupcion\n1, 200 ,0,5\n\n2,150,1,2\n'
        self.assertEqual(parsear_csv(texto), [fila(1, 200, 0, 5), fila(2, 150, 1, 2)])

    def test_fin_de_linea_windows(self):
        self.assertEqual(parsear_csv('id,tamano,arribo,irrupcion\r\n1,200,0,5\r\n'), [fila(1, 200, 0, 5)])

    def test_columnas_de_menos_informa_la_linea(self):
        with self.assertRaisesRegex(ErrorCarga, '2'):
            parsear_csv('id,tamano,arribo,irrupcion\n1,200,0\n')

    def test_valor_no_numerico_informa_la_linea(self):
        with self.assertRaisesRegex(ErrorCarga, '3'):
            parsear_csv('id,tamano,arribo,irrupcion\n1,200,0,5\n2,abc,1,2\n')


class TestValidar(unittest.TestCase):
    def test_lista_valida(self):
        self.assertEqual(validar_procesos([fila(1), fila(2)]), [])

    def test_mas_de_10_procesos(self):
        self.assertTrue(validar_procesos([fila(i) for i in range(1, 12)]))

    def test_lista_vacia(self):
        self.assertTrue(validar_procesos([]))

    def test_junta_todos_los_errores(self):
        errores = validar_procesos([fila(1), fila(1), fila(2, 451), fila(3, 100, -1), fila(4, 100, 0, 0)])
        self.assertGreaterEqual(len(errores), 4)

    def test_tamano_cero(self):
        self.assertTrue(validar_procesos([fila(1, 0)]))


class TestCargarArchivo(unittest.TestCase):
    def test_devuelve_procesos(self):
        procesos = cargar_archivo(str(EJEMPLO))
        self.assertEqual(len(procesos), 4)
        self.assertTrue(all(isinstance(p, Proceso) for p in procesos))
        self.assertEqual(procesos[2].tamano, 300)


class TestCargaManual(unittest.TestCase):
    def test_carga_y_repregunta_datos_invalidos(self):
        # cantidad=2 ; P1: tamaño "abc" (inválido) -> 200, arribo 0, irrupción 5 ; P2: 999 (inválido) -> 150, 1, 2
        respuestas = iter(['2', 'abc', '200', '0', '5', '999', '150', '1', '2', 'n', 'n', 'n'])
        procesos = carga_manual(entrada=lambda *_: next(respuestas))
        self.assertEqual([(p.id, p.tamano, p.arribo, p.irrupcion) for p in procesos],
                         [(1, 200, 0, 5), (2, 150, 1, 2)])


if __name__ == '__main__':
    unittest.main()
