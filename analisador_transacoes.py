import json
from bianca.parametros import obter_parametros
from bianca.modelo import ModeloIA
from util.util import carregar_arquivo
from util.util import salvar_arquivo
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam


def analisar_transacoes(transacao: str, modelo: ModeloIA) -> dict:
    print("1. Executando a análise de transação")

    prompt_sistema = """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada".
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro

        Adote o formato de resposta abaixo para compor sua resposta.

    # Formato Saída
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    }
    """

    prompt_usuario = f"""Considere o CSV abaixo, onde cada linha é uma transação diferente: {transacao}. \
        Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)"""

    lista_mensagens = [
        ChatCompletionSystemMessageParam(
            role="system", content=prompt_sistema),
        ChatCompletionUserMessageParam(role="user", content=transacao)
    ]

    # Temperatura baixa para reduzir a variação na resposta.
    # Dado que esperamos um formato de JSON preciso e não é necessário ser criativo,
    # buscamos estabelecer um comportamento determinístico.
    resposta = modelo.cliente.chat.completions.create(
        model=modelo.modelo,
        messages=lista_mensagens,
        temperature=0
    )
    texto_resposta = resposta.choices[0].message.content
    if texto_resposta:
        texto_resposta = texto_resposta.replace("'", '"')
        print("Conteúdo da resposta: ", texto_resposta + "\n")

        json_resultado = json.loads(texto_resposta)
        print("JSON:", json_resultado)
        return json_resultado
    else:
        print("⚠️ Nenhuma resposta recebida para as transações")
        return {}


def gerar_parecer(transacao: dict, modelo: ModeloIA) -> str:
    print("2. Executando a geração de parecer")

    prompt_sistema = f"""
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer uma justificativa para que você identifique uma fraude.
    Transação: {transacao}

    ## Formato de Resposta
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horario": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localizacao": "cidade - estado (País)"
    "status": "",
    "parecer" : "Colocar Não Aplicável se o status for Aprovado"
    """

    lista_mensagens = [
        ChatCompletionSystemMessageParam(
            role="system", content=prompt_sistema)
        # ,ChatCompletionUserMessageParam(role="user", content=transacao)
    ]

    resposta = modelo.cliente.chat.completions.create(
        model=modelo.modelo,
        messages=lista_mensagens,
        temperature=0
    )
    texto_resposta = resposta.choices[0].message.content
    if texto_resposta:
        return texto_resposta
    else:
        print("⚠️ Nenhuma parecer recebido para a transação")
        return ""


def gerar_recomendacoes(parecer: str, modelo: ModeloIA) -> str:
    print("3. Executando a geração de recomendações")

    prompt_sistema = f"""
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação da Transação: {parecer}

    As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
    Elas devem ser escritas no formato técnico.

    Inclua também uma classificação do tipo de fraude, se aplicável.
    """
    lista_mensagens = [
        ChatCompletionSystemMessageParam(
            role="system", content=prompt_sistema)
        # ,ChatCompletionUserMessageParam(role="user", content=transacao)
    ]
    resposta = modelo.cliente.chat.completions.create(
        model=modelo.modelo,
        messages=lista_mensagens,
        temperature=0
    )
    texto_resposta = resposta.choices[0].message.content
    if texto_resposta:
        return texto_resposta
    else:
        print("⚠️ Nenhuma recomendacao recebida para o parecer")
        return ""


# Obtém a instância de parâmetros
parametros = obter_parametros()
modelo = ModeloIA("gpt-4", parametros)

lista_de_transacoes = carregar_arquivo(f"./dados/transacoes.csv")
transacoes_analisadas = analisar_transacoes(lista_de_transacoes, modelo)

for transacao in transacoes_analisadas['transacoes']:
    if transacao['status'] == "Possível Fraude":
        um_parecer = gerar_parecer(transacao, modelo)
        uma_recomendacao = gerar_recomendacoes(um_parecer, modelo)
        salvar_arquivo(
            (
                f"./dados/"
                f"{transacao['id']}-"
                f"{transacao['nome_produto']}-"
                f"{transacao['status']}.txt"
            ),
            uma_recomendacao
        )
