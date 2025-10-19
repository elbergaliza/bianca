from openai import OpenAI
from dotenv import load_dotenv
import os

# Criacao da API_KEY
# https://platform.openai.com/api-keys

load_dotenv()  # Carrega as variaveis de ambiente do arquivo .env
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4o"


def categoriza_produto(categorias: str, conteudo: str) -> str:
    '''
        Categoriza um produto com base nas categorias fornecidas.'''
    pasta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": f"""
            Classifique o produto abaixo em uma das categorias: 
            {categorias.split(', ')}
            """
            },
            {
                "role": "user",
                "content": f"""
            {conteudo}
            """
            }
        ],
        temperature=0,
        max_tokens=200,
        # NOTE: n=3 para retornar apenas uma resposta
        # n=3
    )
    return pasta.choices[0].message.content or ""


i_categorias = input("Entre as Categorias separadas por virgulas: ")

while True:
    i_conteudo = input("Entre o conteudo do produto: ")
    print(f"Categoria: {categoriza_produto(i_categorias, i_conteudo)}")

# print(resposta.choices[0].message.content)
# print(resposta)

# NOTE: para retornar todas as respostas
# for escolha in resposta.choices:
#    print(escolha.message.content)
