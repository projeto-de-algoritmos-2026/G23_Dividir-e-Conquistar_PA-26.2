"""Núcleo do Preço Justo, independente da interface."""
from .core import analisar_oferta, mediana, selecionar
from .historico import carregar_csv, filtrar_historico

__all__ = ['analisar_oferta', 'mediana', 'selecionar', 'carregar_csv', 'filtrar_historico']
