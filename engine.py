"""Contrato com o núcleo de seleção."""
from importlib.util import find_spec
from pathlib import Path
import sys

# Permite executar a interface diretamente na raiz do projeto.
sys.path.insert(0, str(Path(__file__).parent))

def disponivel():
    return find_spec('preco_justo') is not None

def analisar(precos, oferta):
    if not disponivel():
        raise ValueError('Núcleo pendente: a pasta preco_justo não foi encontrada na raiz.')
    from preco_justo import analisar_oferta
    return analisar_oferta(precos, oferta, incluir_etapas=True)

def importar(texto):
    import csv
    import io
    from datetime import date
    from decimal import Decimal
    leitor = csv.DictReader(io.StringIO(texto.lstrip('\ufeff')), delimiter=';')
    if not {'produto', 'loja', 'data', 'preco'}.issubset(leitor.fieldnames or []):
        raise ValueError('Cabeçalho esperado: produto;loja;data;preco')
    registros = []
    for linha, r in enumerate(leitor, 2):
        try:
            valor = Decimal(r['preco'].strip().replace(',', '.')) * 100
            if not valor.is_finite() or valor <= 0 or valor != valor.to_integral_value():
                raise ValueError()
            registros.append({'produto': r['produto'].strip(), 'loja': r['loja'].strip(),
                              'data': date.fromisoformat(r['data'].strip()).isoformat(),
                              'preco_centavos': int(valor)})
            if not registros[-1]['produto'] or not registros[-1]['loja']:
                raise ValueError()
        except Exception:
            raise ValueError(f'Linha {linha}: registro inválido.') from None
    return registros
