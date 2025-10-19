from openai import OpenAI
from dotenv import load_dotenv
import os

# Criacao da API_KEY
# https://platform.openai.com/api-keys

load_dotenv()  # Carrega as variaveis de ambiente do arquivo .env
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resposta = cliente.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "Listar apenas os nomes dos produtos, sem considerar descrição."
        },
        {
            "role": "user",
            "content": "Liste 3 produtos sustentáveis"
        }
    ]
)

print(resposta.choices[0].message.content)
# print(resposta)
