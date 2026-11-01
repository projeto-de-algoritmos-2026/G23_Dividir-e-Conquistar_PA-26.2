import tempfile
import unittest
from pathlib import Path
from preco_justo import carregar_csv, filtrar_historico


class TestHistorico(unittest.TestCase):
    def ler(self, texto):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / 'dados.csv'
            arquivo.write_text(texto, encoding='utf-8')
            return carregar_csv(arquivo)

    def test_importacao_e_filtro(self):
        registros = self.ler('produto;loja;data;preco\nCafé 500g;A;2026-10-01;12,99\nCafé 500g;B;2026-10-02;13.50\nArroz;A;2026-10-01;20\n')
        self.assertEqual(registros[0]['preco_centavos'], 1299)
        filtro = filtrar_historico(registros, 'CAFÉ 500G', '2026-10-01', '2026-10-01')
        self.assertEqual(len(filtro), 1)
        self.assertEqual(len(filtrar_historico(registros, 'inexistente')), 0)
        with self.assertRaises(ValueError):
            filtrar_historico(registros, 'Café', '2026-10-03', '2026-10-01')

    def test_csv_invalido(self):
        with self.assertRaises(ValueError):
            self.ler('produto;preco\nCafé;10\n')
        for preco in ['NaN', 'Infinity', '-1', '0', '1,001', 'abc']:
            with self.assertRaisesRegex(ValueError, 'Linha 2'):
                self.ler(f'produto;loja;data;preco\nCafé;A;2026-10-01;{preco}\n')
        with self.assertRaises(ValueError):
            self.ler('produto;loja;data;preco\nCafé;A;2026-02-30;10\n')
