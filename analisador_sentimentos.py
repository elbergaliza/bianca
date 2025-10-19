from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from bianca.parametros import obter_parametros
from bianca.modelo import ModeloIA
from util.util import carregar_arquivo, salvar_arquivo

# Obtém a instância de parâmetros
parametros = obter_parametros()
modelo = ModeloIA("gpt-4", parametros)


lista_de_produtos = ["Camisetas de algodão orgânico",
                     "Jeans feitos com materiais reciclados", "Maquiagem mineral"]


def analisar_sentimentos():
    """
    Analisa o sentimento das avaliações de todos os produtos da lista_de_produtos.
    """
    for produto in lista_de_produtos:
        prompt_sistema = """
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
        """
        try:
            prompt_usuario = carregar_arquivo(
                f"./dados/avaliacoes-{produto}.txt")
        except Exception as e:
            print(e)
            continue

        print(f"Iniciou a análise de sentimentos do produto {produto}")

        lista_mensagens = [
            ChatCompletionSystemMessageParam(
                role="system", content=prompt_sistema),
            ChatCompletionUserMessageParam(role="user", content=prompt_usuario)
        ]

        resposta = modelo.cliente.chat.completions.create(
            model=modelo.modelo,
            messages=lista_mensagens
        )
        texto_resposta = resposta.choices[0].message.content

        # Verifica se há resposta antes de salvar
        if texto_resposta:
            salvar_arquivo(f"./dados/analise-{produto}.txt", texto_resposta)
        else:
            print(f"⚠️ Nenhuma resposta recebida para o produto {produto}")


analisar_sentimentos()
