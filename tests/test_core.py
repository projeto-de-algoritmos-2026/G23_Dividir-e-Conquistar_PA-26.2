import random
import unittest
from decimal import Decimal
from preco_justo import analisar_oferta, mediana, selecionar


class TestSelecao(unittest.TestCase):
    def test_contra_ordenacao_em_dados_variados(self):
        rng = random.Random(42)
        for n in [1, 2, 5, 6, 25, 51, 200]:
            for dados in [list(range(1, n + 1)), list(range(n, 0, -1)),
                          [7] * n, [rng.randint(1, 1000) for _ in range(n)]]:
                original = dados.copy()
                esperado = sorted(dados)
                for k in range(n):
                    self.assertEqual(selecionar(dados, k), esperado[k])
                centro = (Decimal(esperado[(n - 1) // 2]) + Decimal(esperado[n // 2])) / 2
                self.assertEqual(mediana(dados), centro)
                self.assertEqual(dados, original)

    def test_precisao_e_classificacao(self):
        self.assertEqual(mediana([100, 101]), Decimal('100.5'))
        r = analisar_oferta([1200, 1300, 1400, 1500, 1600, 1800, 4000], 1300, True)
        self.assertEqual(r['mediana_centavos'], '1500')
        self.assertEqual(r['variacao_percentual'], '-13.33')
        self.assertEqual(r['situacao'], 'abaixo')
        self.assertTrue(any(e['tipo'] == 'particao' for e in r['etapas']))
        self.assertEqual(analisar_oferta([100], 100)['situacao'], 'igual')
        self.assertEqual(analisar_oferta([100], 200)['situacao'], 'acima')

    def test_entradas_invalidas(self):
        for dados in [[], [0], [-1], [True], [1.5], ['100']]:
            with self.assertRaises(ValueError):
                mediana(dados)
        for k in [-1, 1, True, 0.5]:
            with self.assertRaises(ValueError):
                selecionar([100], k)
        with self.assertRaises(ValueError):
            analisar_oferta([100], 0)
