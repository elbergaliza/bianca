"""
Calculadora de Tokens e Comparação de Custos entre Modelos de IA
Utiliza o módulo parametros.py para realizar cálculos precisos de custos
e comparações entre diferentes modelos de IA.

FUNCIONALIDADES INCLUÍDAS:
- Contagem de tokens para diferentes modelos
- Cálculo de custos (entrada, saída, total)
- Verificação de limites de tokens
- Comparação de modelos (custos e configurações)
- Análise detalhada de custos
- Identificação do modelo mais econômico

Integrado com parametros.py para configurações dos modelos.
"""

import tiktoken
from typing import Dict, List, Optional, Tuple, Any
from bianca.parametros import obter_parametros


class CalculadoraTokens:
    """Classe para calcular tokens e custos de modelos de IA"""

    def __init__(self):
        self.parametros = obter_parametros()

    def contar_tokens(self, texto: str, modelo: str) -> int:
        """
        Conta o número de tokens em um texto para um modelo específico

        Args:
            texto: Texto para contar tokens
            modelo: Nome do modelo de IA

        Returns:
            Número de tokens
        """
        try:
            codificador = tiktoken.encoding_for_model(modelo)
            return len(codificador.encode(texto))
        except KeyError:
            # Fallback para GPT-4 se o modelo não for reconhecido
            codificador = tiktoken.get_encoding("cl100k_base")
            return len(codificador.encode(texto))

    def calcular_custo_completo(self, texto_entrada: str, modelo: str,
                                tokens_resposta: int = 100) -> Dict[str, float]:
        """
        Calcula o custo completo de uma requisição

        Args:
            texto_entrada: Texto de entrada
            modelo: Nome do modelo
            tokens_resposta: Número estimado de tokens na resposta

        Returns:
            Dicionário com custos detalhados
        """
        tokens_entrada = self.contar_tokens(texto_entrada, modelo)

        custo_entrada = self.calcular_custo(modelo, tokens_entrada, 0)
        custo_saida = self.calcular_custo(modelo, 0, tokens_resposta)
        custo_total = custo_entrada + custo_saida

        return {
            'tokens_entrada': tokens_entrada,
            'tokens_saida': tokens_resposta,
            'custo_entrada': custo_entrada,
            'custo_saida': custo_saida,
            'custo_total': custo_total
        }

    def comparar_custo_modelos(self, texto: str, modelos: List[str],
                               tokens_resposta: int = 100) -> Dict[str, Dict]:
        """
        Compara o custo de diferentes modelos para o mesmo texto

        Args:
            texto: Texto para análise
            modelos: Lista de nomes de modelos para comparar
            tokens_resposta: Número estimado de tokens na resposta

        Returns:
            Dicionário com comparação detalhada
        """
        resultados = {}

        for modelo in modelos:
            if modelo in self.parametros.listar_modelos_disponiveis():
                custo_info = self.calcular_custo_completo(
                    texto, modelo, tokens_resposta)
                resultados[modelo] = custo_info
            else:
                print(
                    f"AVISO: Modelo '{modelo}' nao encontrado nos parametros configurados")

        return resultados

    def encontrar_modelo_mais_economico(self, texto: str, modelos: List[str],
                                        tokens_resposta: int = 100) -> Tuple[str, float]:
        """
        Encontra o modelo mais econômico para um texto específico

        Args:
            texto: Texto para análise
            modelos: Lista de modelos para comparar
            tokens_resposta: Número estimado de tokens na resposta

        Returns:
            Tupla com (nome_do_modelo, custo_total)
        """
        comparacao = self.comparar_custo_modelos(
            texto, modelos, tokens_resposta)

        if not comparacao:
            raise ValueError("Nenhum modelo válido encontrado para comparação")

        modelo_mais_barato = min(comparacao.keys(),
                                 key=lambda x: comparacao[x]['custo_total'])

        return modelo_mais_barato, comparacao[modelo_mais_barato]['custo_total']

    def calcular_custo(self, nome_modelo: str, tokens_entrada: int, tokens_saida: int = 0) -> float:
        """
        Calcula o custo de uma requisição baseado no modelo e número de tokens

        Args:
            nome_modelo: Nome do modelo a ser usado
            tokens_entrada: Número de tokens de entrada
            tokens_saida: Número de tokens de saída

        Returns:
            Custo total em dólares
        """
        modelo = self.parametros.obter_modelo(nome_modelo)
        if not modelo:
            raise ValueError(f"Modelo '{nome_modelo}' não encontrado")

        custo_entrada = (tokens_entrada / 1000) * \
            modelo.preco_entrada_por_1k_tokens
        custo_saida = (tokens_saida / 1000) * modelo.preco_saida_por_1k_tokens

        return custo_entrada + custo_saida

    def verificar_limite_tokens(self, nome_modelo: str, tokens_entrada: int, tokens_saida: int = 0) -> bool:
        """
        Verifica se o número de tokens está dentro do limite do modelo

        Args:
            nome_modelo: Nome do modelo
            tokens_entrada: Número de tokens de entrada
            tokens_saida: Número de tokens de saída

        Returns:
            True se está dentro do limite, False caso contrário
        """
        modelo = self.parametros.obter_modelo(nome_modelo)
        if not modelo:
            return False

        return (tokens_entrada + tokens_saida) <= modelo.limite_tokens

    def mostrar_comparacao_detalhada(self, texto: str, modelos: Optional[List[str]] = None,
                                     tokens_resposta: int = 100):
        """
        Exibe uma comparação detalhada dos modelos

        Args:
            texto: Texto para análise
            modelos: Lista de modelos (se None, usa todos os disponíveis)
            tokens_resposta: Número estimado de tokens na resposta
        """
        if modelos is None:
            modelos = self.parametros.listar_modelos_disponiveis()

        print(f"ANALISE DE CUSTOS PARA O TEXTO:")
        print(f"'{texto[:100]}{'...' if len(texto) > 100 else ''}'\n")

        comparacao = self.comparar_custo_modelos(
            texto, modelos, tokens_resposta)

        if not comparacao:
            print("ERRO: Nenhum modelo valido encontrado")
            return

        # Cabeçalho da tabela
        print(f"{'Modelo':<20} {'Tokens Entrada':<15} {'Custo Entrada':<15} {'Custo Saida':<15} {'Custo Total':<15}")
        print("-" * 85)

        # Dados dos modelos
        for modelo, dados in comparacao.items():
            print(f"{modelo:<20} {dados['tokens_entrada']:<15} "
                  f"${dados['custo_entrada']:.6f}{'':<8} "
                  f"${dados['custo_saida']:.6f}{'':<8} "
                  f"${dados['custo_total']:.6f}")

        # Encontrar e destacar o mais econômico
        modelo_barato, custo_barato = self.encontrar_modelo_mais_economico(
            texto, modelos, tokens_resposta)

        print("\n" + "="*85)
        print(f"MODELO MAIS ECONOMICO: {modelo_barato} (${custo_barato:.6f})")

        # Mostrar diferenças percentuais
        print("\nDIFERENCAS EM RELACAO AO MODELO MAIS BARATO:")
        for modelo, dados in comparacao.items():
            if modelo != modelo_barato:
                diferenca = (
                    (dados['custo_total'] - custo_barato) / custo_barato) * 100
                print(f"{modelo}: {diferenca:.1f}% mais caro")


def main():
    """Função principal para demonstração"""
    calculadora = CalculadoraTokens()

    # Texto de exemplo
    texto_exemplo = "Você é um categorizador de produtos. Analise o seguinte produto e categorize-o adequadamente."

    print("CALCULADORA DE TOKENS E COMPARACAO DE CUSTOS\n")

    # Exemplo 1: Analise simples com dois modelos
    print("=" * 60)
    print("EXEMPLO 1: Comparacao entre GPT-4 e GPT-3.5-Turbo")
    print("=" * 60)

    modelos_teste = ['gpt-4', 'gpt-3.5-turbo']
    calculadora.mostrar_comparacao_detalhada(texto_exemplo, modelos_teste)

    # Exemplo 2: Comparacao com todos os modelos disponiveis
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Comparacao com todos os modelos disponiveis")
    print("=" * 60)

    calculadora.mostrar_comparacao_detalhada(texto_exemplo)

    # Exemplo 3: Analise com diferentes tamanhos de resposta
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Impacto do tamanho da resposta no custo")
    print("=" * 60)

    tamanhos_resposta = [50, 100, 200, 500]
    for tamanho in tamanhos_resposta:
        print(f"\nResposta com {tamanho} tokens:")
        modelo_barato, custo = calculadora.encontrar_modelo_mais_economico(
            texto_exemplo, ['gpt-4', 'gpt-3.5-turbo'], tamanho
        )
        print(f"   Modelo mais economico: {modelo_barato} (${custo:.6f})")


if __name__ == "__main__":
    main()
