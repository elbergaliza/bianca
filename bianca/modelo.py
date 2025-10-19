"""
Módulo de modelo de IA - BIANCA
Biblioteca de Inteligência Artificial para Novos Componentes e Aplicações

Este modulo gerencia um modelo específico de IA.
"""
# TODO: Implementar a classe ModeloIA para gerenciar um modelo específico de IA. Uma forma é especializar essa classe para colocar caracteristicas
# específicas de cada modelo de IA.

from openai import OpenAI  # Adiciona importação de OpenAI no escopo correto
from bianca.parametros import ParametrosIA


class ModeloIA:
    """Classe para gerenciar um modelo específico"""

    def __init__(self, modelo: str, parametros_ia: ParametrosIA):
        if modelo not in parametros_ia.listar_modelos_disponiveis():
            raise ValueError(
                f"Modelo '{modelo}' não está na lista de modelos disponíveis: {parametros_ia.listar_modelos_disponiveis()}")
        self.modelo = modelo
        self.parametros_ia = parametros_ia
        self.cliente = OpenAI(api_key=self.parametros_ia.obter_chave_api())

    def obter_modelo(self) -> str:
        """Retorna o modelo"""
        return self.modelo

    def definir_modelo(self, modelo: str) -> None:
        """Define o modelo"""
        self.modelo = modelo

    def obter_cliente(self) -> OpenAI:
        """Retorna o cliente"""
        return self.cliente
