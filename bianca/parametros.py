"""
Módulo de Configurações de IA - BIANCA
Biblioteca de Inteligência Artificial para Novos Componentes e Aplicações

Este módulo centraliza APENAS as configurações básicas de IA, incluindo:
- Configurações de modelos (preços, limites, temperaturas)
- Configurações de API (chave, timeouts)
- Configurações gerais do sistema

FUNCIONALIDADES DE CÁLCULO E COMPARAÇÃO foram movidas para calcular_tokens.py

Modelos incluídos:
- GPT-4 e GPT-4 Turbo (modelos clássicos)
- GPT-4o e GPT-4o-mini (modelos otimizados mais recentes)
- o1-preview e o1-mini (modelos de raciocínio)
- GPT-3.5 Turbo (versões variadas)
- Modelos de Embeddings (text-embedding-3-small/large)
- Modelos de Moderação (text-moderation-latest)

Refatorado em: Dezembro 2024
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    # Carrega variáveis de ambiente
    load_dotenv()
except ImportError as e:
    print("Erro ao carregar o arquivo .env")
    raise e
    # Se dotenv não estiver disponível, continua sem carregar
    pass


@dataclass
class ModeloConfig:
    """Configuração de um modelo de IA"""
    nome: str
    preco_entrada_por_1k_tokens: float  # Preço por 1000 tokens de entrada
    preco_saida_por_1k_tokens: float    # Preço por 1000 tokens de saída
    limite_tokens: int                  # Limite máximo de tokens
    temperatura_padrao: float          # Temperatura padrão
    max_tokens_resposta: int           # Número máximo de tokens na resposta
    descricao: str                     # Descrição do modelo


class ParametrosIA:
    """Classe principal para gerenciar parâmetros de IA"""

    def __init__(self):
        self.chave_api = os.getenv('OPENAI_API_KEY', '')
        if not self.chave_api:
            raise ValueError("A chave da API não está preenchida")
        self.modelo = None  # Modelo atualmente selecionado
        self.tempo_espera_padrao = 30  # segundos
        self.temperatura_padrao = 0.7
        self.max_tokens_padrao = 1000

        # Configurações dos modelos - Atualizados com modelos mais recentes da OpenAI
        self.modelos = {
            # Modelos GPT-4 (mais antigos, ainda disponíveis)
            'gpt-4': ModeloConfig(
                nome='gpt-4',
                preco_entrada_por_1k_tokens=0.03,
                preco_saida_por_1k_tokens=0.06,
                limite_tokens=8192,
                temperatura_padrao=0.7,
                max_tokens_resposta=4096,
                descricao='Modelo GPT-4 original, ideal para tarefas complexas'
            ),
            'gpt-4-turbo': ModeloConfig(
                nome='gpt-4-turbo',
                preco_entrada_por_1k_tokens=0.01,
                preco_saida_por_1k_tokens=0.03,
                limite_tokens=128000,
                temperatura_padrao=0.7,
                max_tokens_resposta=4096,
                descricao='Versão turbo do GPT-4 com contexto expandido'
            ),

            # Modelos GPT-4o (mais recentes)
            'gpt-4o': ModeloConfig(
                nome='gpt-4o',
                preco_entrada_por_1k_tokens=0.005,
                preco_saida_por_1k_tokens=0.015,
                limite_tokens=128000,
                temperatura_padrao=0.7,
                max_tokens_resposta=4096,
                descricao='Modelo GPT-4o otimizado, mais rápido e econômico que GPT-4'
            ),
            'gpt-4o-mini': ModeloConfig(
                nome='gpt-4o-mini',
                preco_entrada_por_1k_tokens=0.00015,
                preco_saida_por_1k_tokens=0.0006,
                limite_tokens=128000,
                temperatura_padrao=0.7,
                max_tokens_resposta=16384,
                descricao='Versão mini do GPT-4o, extremamente econômica'
            ),

            # Modelos o1 (raciocínio)
            'o1-preview': ModeloConfig(
                nome='o1-preview',
                preco_entrada_por_1k_tokens=0.15,
                preco_saida_por_1k_tokens=0.60,
                limite_tokens=128000,
                temperatura_padrao=0.7,
                max_tokens_resposta=4096,
                descricao='Modelo o1 para raciocínio complexo e programação'
            ),
            'o1-mini': ModeloConfig(
                nome='o1-mini',
                preco_entrada_por_1k_tokens=0.075,
                preco_saida_por_1k_tokens=0.30,
                limite_tokens=128000,
                temperatura_padrao=0.7,
                max_tokens_resposta=4096,
                descricao='Versão mini do o1, mais econômica para raciocínio'
            ),

            # Modelos GPT-3.5
            'gpt-3.5-turbo': ModeloConfig(
                nome='gpt-3.5-turbo',
                preco_entrada_por_1k_tokens=0.001,
                preco_saida_por_1k_tokens=0.002,
                limite_tokens=16384,
                temperatura_padrao=0.7,
                max_tokens_resposta=4096,
                descricao='Modelo econômico e eficiente para tarefas gerais'
            ),
            'gpt-3.5-turbo-1106': ModeloConfig(
                nome='gpt-3.5-turbo-1106',
                preco_entrada_por_1k_tokens=0.001,
                preco_saida_por_1k_tokens=0.002,
                limite_tokens=16384,
                temperatura_padrao=0.7,
                max_tokens_resposta=4096,
                descricao='Versão 1106 do GPT-3.5 Turbo com melhorias'
            ),
            'gpt-3.5-turbo-0125': ModeloConfig(
                nome='gpt-3.5-turbo-0125',
                preco_entrada_por_1k_tokens=0.0005,
                preco_saida_por_1k_tokens=0.0015,
                limite_tokens=16384,
                temperatura_padrao=0.7,
                max_tokens_resposta=4096,
                descricao='Versão 0125 do GPT-3.5 Turbo, mais econômica'
            ),

            # Modelos de Embeddings
            'text-embedding-3-small': ModeloConfig(
                nome='text-embedding-3-small',
                preco_entrada_por_1k_tokens=0.00002,
                preco_saida_por_1k_tokens=0.0,
                limite_tokens=8191,
                temperatura_padrao=0.0,
                max_tokens_resposta=1536,
                descricao='Modelo de embeddings pequeno e econômico'
            ),
            'text-embedding-3-large': ModeloConfig(
                nome='text-embedding-3-large',
                preco_entrada_por_1k_tokens=0.00013,
                preco_saida_por_1k_tokens=0.0,
                limite_tokens=8191,
                temperatura_padrao=0.0,
                max_tokens_resposta=3072,
                descricao='Modelo de embeddings grande com alta qualidade'
            ),

            # Modelos de Moderação
            'text-moderation-latest': ModeloConfig(
                nome='text-moderation-latest',
                preco_entrada_por_1k_tokens=0.0001,
                preco_saida_por_1k_tokens=0.0,
                limite_tokens=32768,
                temperatura_padrao=0.0,
                max_tokens_resposta=1,
                descricao='Modelo para moderação de conteúdo'
            )
        }

    def obter_chave_api(self) -> str:
        """Retorna a chave da API"""
        return self.chave_api

    def definir_chave_api(self, chave: str) -> None:
        """Define a chave da API"""
        self.chave_api = chave

    def obter_modelo(self, nome_modelo: str) -> Optional[ModeloConfig]:
        """Retorna a configuração de um modelo específico"""
        return self.modelos.get(nome_modelo)

    def listar_modelos(self) -> Dict[str, ModeloConfig]:
        """Retorna todos os modelos configurados"""
        return self.modelos.copy()

    def listar_modelos_disponiveis(self) -> List[str]:
        """Retorna nomes dos modelos disponíveis"""
        return list(self.modelos.keys())

    def obter_tempo_espera(self) -> int:
        """Retorna o tempo de espera padrão em segundos"""
        return self.tempo_espera_padrao

    def definir_tempo_espera(self, segundos: int) -> None:
        """Define o tempo de espera padrão"""
        self.tempo_espera_padrao = segundos

    def obter_temperatura_padrao(self) -> float:
        """Retorna a temperatura padrão"""
        return self.temperatura_padrao

    def definir_temperatura_padrao(self, temperatura: float) -> None:
        """Define a temperatura padrão (0.0 a 2.0)"""
        if 0.0 <= temperatura <= 2.0:
            self.temperatura_padrao = temperatura
        else:
            raise ValueError("Temperatura deve estar entre 0.0 e 2.0")

    def obter_max_tokens_padrao(self) -> int:
        """Retorna o número máximo de tokens padrão para resposta"""
        return self.max_tokens_padrao

    def definir_max_tokens_padrao(self, max_tokens: int) -> None:
        """Define o número máximo de tokens padrão para resposta"""
        self.max_tokens_padrao = max_tokens

    def obter_configuracao_completa(self, nome_modelo: str) -> Dict[str, Any]:
        """
        Retorna a configuração completa para um modelo específico

        Args:
            nome_modelo: Nome do modelo

        Returns:
            Dicionário com todas as configurações
        """
        modelo = self.obter_modelo(nome_modelo)
        if not modelo:
            raise ValueError(f"Modelo '{nome_modelo}' não encontrado")

        return {
            'modelo': modelo.nome,
            'preco_entrada_por_1k_tokens': modelo.preco_entrada_por_1k_tokens,
            'preco_saida_por_1k_tokens': modelo.preco_saida_por_1k_tokens,
            'limite_tokens': modelo.limite_tokens,
            'temperatura_padrao': modelo.temperatura_padrao,
            'max_tokens_resposta': modelo.max_tokens_resposta,
            'descricao': modelo.descricao,
            'tempo_espera_padrao': self.tempo_espera_padrao,
            'chave_api_configurada': bool(self.chave_api)
        }

    def comparar_modelos_configuracao(self, modelo1: str, modelo2: str) -> Dict[str, Any]:
        """
        Compara dois modelos e retorna informações de comparação

        Args:
            modelo1: Nome do primeiro modelo
            modelo2: Nome do segundo modelo

        Returns:
            Dicionário com informações de comparação
        """
        config1 = self.obter_modelo(modelo1)
        config2 = self.obter_modelo(modelo2)

        if not config1 or not config2:
            raise ValueError("Um ou ambos os modelos não foram encontrados")

        return {
            'modelo1': {
                'nome': config1.nome,
                'preco_entrada': config1.preco_entrada_por_1k_tokens,
                'preco_saida': config1.preco_saida_por_1k_tokens,
                'limite_tokens': config1.limite_tokens,
                'descricao': config1.descricao
            },
            'modelo2': {
                'nome': config2.nome,
                'preco_entrada': config2.preco_entrada_por_1k_tokens,
                'preco_saida': config2.preco_saida_por_1k_tokens,
                'limite_tokens': config2.limite_tokens,
                'descricao': config2.descricao
            },
            'comparacao': {
                'diferenca_preco_entrada': config1.preco_entrada_por_1k_tokens - config2.preco_entrada_por_1k_tokens,
                'diferenca_preco_saida': config1.preco_saida_por_1k_tokens - config2.preco_saida_por_1k_tokens,
                'diferenca_limite_tokens': config1.limite_tokens - config2.limite_tokens,
                'modelo_mais_caro': modelo1 if config1.preco_entrada_por_1k_tokens > config2.preco_entrada_por_1k_tokens else modelo2,
                'modelo_mais_barato': modelo1 if config1.preco_entrada_por_1k_tokens < config2.preco_entrada_por_1k_tokens else modelo2
            }
        }


# Instância global para uso em toda a aplicação
parametros_ia = ParametrosIA()


def obter_parametros() -> ParametrosIA:
    """Função de conveniência para obter a instância global de parâmetros"""
    return parametros_ia
