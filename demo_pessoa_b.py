"""Demonstração executável sem dependências externas."""
import json
from pathlib import Path
from preco_justo import carregar_csv, filtrar_historico, analisar_oferta

if __name__ == '__main__':
    arquivo = Path(__file__).parent / 'exemplos' / 'precos.csv'
    historico = filtrar_historico(carregar_csv(arquivo), 'Café Marca A 500g',
                                 '2026-10-01', '2026-10-26')
    resultado = analisar_oferta([r['preco_centavos'] for r in historico], 1300, True)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
