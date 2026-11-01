"""Leitura e filtro de histórico; um produto deve ter marca e peso definidos."""
import csv
from datetime import date
from decimal import Decimal, InvalidOperation


def carregar_csv(caminho):
    """Lê CSV UTF-8 separado por ponto e vírgula, com preço em reais.

    Colunas: produto;loja;data;preco. Datas ISO: AAAA-MM-DD.
    Aceita decimal com vírgula ou ponto, sem separador de milhares.
    Retorna registros com data ISO e preco_centavos inteiro.
    """
    registros = []
    with open(caminho, encoding='utf-8-sig', newline='') as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=';')
        if not {'produto', 'loja', 'data', 'preco'}.issubset(leitor.fieldnames or []):
            raise ValueError('CSV deve conter produto;loja;data;preco.')
        for linha, item in enumerate(leitor, 2):
            try:
                produto = item['produto'].strip()
                loja = item['loja'].strip()
                dia = date.fromisoformat(item['data'].strip()).isoformat()
                preco = Decimal(item['preco'].strip().replace(',', '.'))
                if not produto or not loja or not preco.is_finite() or preco <= 0:
                    raise ValueError()
                centavos = preco * 100
                if centavos != centavos.to_integral_value():
                    raise ValueError()
                registros.append({'produto': produto, 'loja': loja,
                                  'data': dia, 'preco_centavos': int(centavos)})
            except (ValueError, InvalidOperation, AttributeError, TypeError):
                raise ValueError(f'Linha {linha}: produto, loja, data ou preço inválido.') from None
    return registros


def filtrar_historico(registros, produto, inicio=None, fim=None):
    """Filtra por produto exato (ignorando caixa) e datas inclusivas ISO."""
    inicial = date.fromisoformat(inicio) if inicio else date.min
    final = date.fromisoformat(fim) if fim else date.max
    if inicial > final:
        raise ValueError('Data inicial posterior à final.')
    return [r.copy() for r in registros
            if r['produto'].strip().casefold() == produto.strip().casefold()
            and inicial <= date.fromisoformat(r['data']) <= final]
