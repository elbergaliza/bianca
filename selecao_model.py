from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
import os
from dotenv import load_dotenv
import tiktoken
from typing import List

# Load environment variables and initialize client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"


prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""


def carrega(nome_do_arquivo: str) -> str:
    """
    Carrega o conteúdo de um arquivo e verifica seu tamanho.
    Retorna o conteúdo do arquivo ou lança uma exceção se houver problemas.
    """
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            if not dados:
                raise ValueError("Arquivo está vazio")
            return dados
    except IOError as e:
        raise IOError(f"Erro ao ler arquivo {nome_do_arquivo}: {e}")
    except Exception as e:
        raise Exception(f"Erro inesperado ao processar arquivo: {e}")


prompt_usuario = carrega("dados/lista_de_compras_100_clientes.csv")

# Token counting and model selection
codificador = tiktoken.encoding_for_model(modelo)
lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
numero_de_tokens = len(lista_de_tokens)
print(f"Número de tokens na entrada: {numero_de_tokens}")
tamanho_esperado_saida = 2048

if numero_de_tokens >= 4096 - tamanho_esperado_saida:
    modelo = "gpt-4-1106-preview"

print(f"Modelo escolhido: {modelo}")

# Create messages using helper functions
# lista_mensagens = [
#     create_system_message(prompt_sistema),
#     create_user_message(prompt_usuario)
# ]

lista_mensagens: List[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": prompt_sistema
    },
    {
        "role": "user",
        "content": prompt_usuario
    }
]

# Make API call
resposta = client.chat.completions.create(
    model=modelo,
    messages=lista_mensagens
)

print(resposta.choices[0].message.content)
