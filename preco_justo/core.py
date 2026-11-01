"""Seleção determinística BFPRT e comparação de preços em centavos."""
from decimal import Decimal


def _validar(valores):
    dados = list(valores)
    if not dados:
        raise ValueError('Informe pelo menos um preço.')
    if any(type(v) is not int or v <= 0 for v in dados):
        raise ValueError('Os preços devem ser inteiros positivos em centavos.')
    return dados


def _selecionar(dados, k, etapas):
    if len(dados) <= 5:
        resultado = sorted(dados)[k]
        if etapas is not None:
            etapas.append({'tipo': 'base', 'tamanho': len(dados), 'k': k, 'resultado': resultado})
        return resultado
    grupos = [dados[i:i + 5] for i in range(0, len(dados), 5)]
    medianas = [sorted(g)[len(g) // 2] for g in grupos]
    pivo = _selecionar(medianas, len(medianas) // 2, etapas)
    menores = [v for v in dados if v < pivo]
    iguais = [v for v in dados if v == pivo]
    maiores = [v for v in dados if v > pivo]
    if etapas is not None:
        etapas.append({'tipo': 'particao', 'tamanho': len(dados), 'k': k,
                       'pivo': pivo, 'menores': len(menores),
                       'iguais': len(iguais), 'maiores': len(maiores)})
    if k < len(menores):
        return _selecionar(menores, k, etapas)
    if k < len(menores) + len(iguais):
        return pivo
    return _selecionar(maiores, k - len(menores) - len(iguais), etapas)


def selecionar(valores, k, etapas=None):
    """Retorna o elemento de índice k (base zero); não modifica a entrada.

    etapas: lista opcional que recebe eventos para visualização.
    A ordenação ocorre somente em grupos de até cinco elementos.
    """
    dados = _validar(valores)
    if type(k) is not int or not 0 <= k < len(dados):
        raise ValueError('k deve ser um índice válido, começando em zero.')
    return _selecionar(dados, k, etapas)


def mediana(valores, etapas=None):
    """Retorna Decimal em centavos; permite meio centavo em listas pares."""
    dados = _validar(valores)
    n = len(dados)
    superior = _selecionar(dados, n // 2, etapas)
    if n % 2:
        return Decimal(superior)
    inferior = _selecionar(dados, n // 2 - 1, etapas)
    return (Decimal(inferior) + Decimal(superior)) / 2


def analisar_oferta(precos, oferta_centavos, incluir_etapas=False):
    """Resultado serializável em JSON para consumo da interface.

    Percentual positivo significa oferta acima da mediana; negativo, abaixo.
    Valores decimais saem como strings para preservar a precisão monetária.
    """
    dados = _validar(precos)
    _validar([oferta_centavos])
    etapas = [] if incluir_etapas else None
    central = mediana(dados, etapas)
    diferenca = Decimal(oferta_centavos) - central
    percentual = (diferenca / central * 100).quantize(Decimal('0.01'))
    situacao = 'abaixo' if diferenca < 0 else 'acima' if diferenca > 0 else 'igual'
    resultado = {
        'quantidade': len(dados), 'mediana_centavos': str(central),
        'mediana_reais': str((central / 100).quantize(Decimal('0.01'))),
        'oferta_centavos': oferta_centavos,
        'diferenca_centavos': str(diferenca),
        'variacao_percentual': str(percentual), 'situacao': situacao,
        'mensagem': f'Oferta {situacao} da mediana do histórico.' if situacao != 'igual'
                    else 'Oferta igual à mediana do histórico.'}
    if incluir_etapas:
        resultado['etapas'] = etapas
    return resultado
