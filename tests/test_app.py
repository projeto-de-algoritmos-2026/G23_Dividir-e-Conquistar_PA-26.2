import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import engine
import storage

class TestAplicacao(unittest.TestCase):
    def test_csv_e_persistencia(self):
        dados = engine.importar('produto;loja;data;preco\nCafé 500g;Loja A;2026-10-01;12,99\n')
        with tempfile.TemporaryDirectory() as pasta, patch.object(storage, 'DB', Path(pasta) / 'teste.sqlite3'):
            storage.salvar(dados)
            self.assertEqual(storage.listar()[0]['preco_centavos'], 1299)
            with self.assertRaises(ValueError):
                storage.salvar([dict(dados[0], preco_centavos=0)])
            self.assertEqual(len(storage.listar()), 1)

    def test_csv_invalido(self):
        for preco in ['NaN', 'Infinity', '-1', '0', '12.001', 'abc']:
            with self.assertRaises(ValueError):
                engine.importar(f'produto;loja;data;preco\nCafé;Loja;2026-10-01;{preco}\n')

    def test_nucleo_pendente(self):
        with patch.object(engine, 'disponivel', return_value=False):
            with self.assertRaisesRegex(ValueError, 'Núcleo pendente'):
                engine.analisar([100], 90)
