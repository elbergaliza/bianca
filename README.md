# BIANCA - Biblioteca de Inteligência Artificial para Novos Componentes e Aplicações

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/bianca-ai.svg)](https://badge.fury.io/py/bianca-ai)

BIANCA é uma biblioteca Python que facilita o trabalho com modelos de IA da OpenAI, oferecendo funcionalidades para cálculo de tokens, comparação de custos e configurações centralizadas.

## 🚀 Características Principais

- **Cálculo Preciso de Tokens**: Contagem de tokens para diferentes modelos usando tiktoken
- **Comparação de Custos**: Análise detalhada de custos entre modelos
- **Configurações Centralizadas**: Gerenciamento unificado de parâmetros de IA
- **Modelos Atualizados**: Suporte aos modelos mais recentes da OpenAI
- **Fácil Integração**: API simples e intuitiva

## 📦 Instalação

### Instalação via pip (recomendado)

```bash
pip install bianca-ai
```

### Instalação do código fonte

```bash
git clone https://github.com/your-username/bianca-ai.git
cd bianca-ai
pip install -e .
```

### Instalação com dependências extras

```bash
# Para desenvolvimento
pip install bianca-ai[dev]

# Para funcionalidades de áudio
pip install bianca-ai[audio]

# Todas as dependências
pip install bianca-ai[all]
```

## 🎯 Uso Rápido

### Exemplo Básico

```python
from bianca import CalculadoraTokens, obter_parametros

# Criar calculadora
calc = CalculadoraTokens()

# Calcular custo de um texto
texto = "Analise este produto e categorize-o"
custo_info = calc.calcular_custo_completo(texto, 'gpt-4o', 100)
print(f"Custo total: ${custo_info['custo_total']:.6f}")

# Comparar modelos
modelo_barato, custo = calc.encontrar_modelo_mais_economico(
    texto, ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo'], 100
)
print(f"Modelo mais econômico: {modelo_barato}")
```

### Comparação de Modelos

```python
from bianca import CalculadoraTokens

calc = CalculadoraTokens()

# Comparar custos entre modelos
texto = "Você é um assistente de IA especializado em análise de dados."
calc.mostrar_comparacao_detalhada(texto, ['gpt-4o', 'gpt-4o-mini'])
```

### Configurações

```python
from bianca import obter_parametros

# Obter configurações
params = obter_parametros()
modelos = params.listar_modelos_disponiveis()
print(f"Modelos disponíveis: {modelos}")

# Obter configuração específica
config = params.obter_modelo('gpt-4o')
print(f"Preço GPT-4o: ${config.preco_entrada_por_1k_tokens}/1k tokens")
```

## 📚 Modelos Suportados

### Modelos GPT-4
- `gpt-4`: Modelo original GPT-4
- `gpt-4-turbo`: Versão turbo com contexto expandido
- `gpt-4o`: Modelo otimizado mais recente
- `gpt-4o-mini`: Versão mini extremamente econômica

### Modelos o1 (Raciocínio)
- `o1-preview`: Para raciocínio complexo
- `o1-mini`: Versão mais econômica para raciocínio

### Modelos GPT-3.5
- `gpt-3.5-turbo`: Modelo econômico geral
- `gpt-3.5-turbo-1106`: Versão com melhorias
- `gpt-3.5-turbo-0125`: Versão mais recente

### Modelos Especializados
- `text-embedding-3-small`: Embeddings pequenos
- `text-embedding-3-large`: Embeddings grandes
- `text-moderation-latest`: Moderação de conteúdo

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do seu projeto:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

### Configuração Programática

```python
from bianca import ParametrosIA

# Criar instância personalizada
params = ParametrosIA()
params.definir_temperatura_padrao(0.5)
params.definir_max_tokens_padrao(2000)
```

## 📖 API Reference

### CalculadoraTokens

#### `calcular_custo(modelo, tokens_entrada, tokens_saida=0)`
Calcula o custo total para um modelo específico.

#### `contar_tokens(texto, modelo)`
Conta o número de tokens em um texto.

#### `verificar_limite_tokens(modelo, tokens_entrada, tokens_saida=0)`
Verifica se o número de tokens está dentro do limite do modelo.

#### `comparar_modelos(texto, modelos, tokens_resposta=100)`
Compara custos entre múltiplos modelos.

#### `encontrar_modelo_mais_economico(texto, modelos, tokens_resposta=100)`
Encontra o modelo mais econômico para um texto específico.

### ParametrosIA

#### `listar_modelos_disponiveis()`
Retorna lista de todos os modelos disponíveis.

#### `obter_modelo(nome_modelo)`
Retorna configuração de um modelo específico.

#### `obter_configuracao_completa(nome_modelo)`
Retorna configuração completa incluindo metadados.

## 🧪 Testes

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=bianca

# Testes específicos
pytest tests/test_calcular_tokens.py
```

## 🛠️ Desenvolvimento

### Configurar Ambiente de Desenvolvimento

```bash
# Clonar repositório
git clone https://github.com/your-username/bianca-ai.git
cd bianca-ai

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências de desenvolvimento
pip install -e .[dev]
```

### Estrutura do Projeto

```
bianca-ai/
├── bianca/                 # Módulo principal
│   ├── __init__.py        # Inicialização do módulo
│   ├── parametros.py      # Configurações e parâmetros
│   ├── calcular_tokens.py # Cálculo de tokens e custos
│   ├── modelo.py          # Classes de modelos
│   └── converter_audio_texto.py  # Conversão de áudio
├── tests/                 # Testes
├── docs/                  # Documentação
├── examples/              # Exemplos de uso
├── setup.py               # Configuração de instalação
├── pyproject.toml         # Configuração moderna
├── requirements.txt       # Dependências
└── README.md             # Este arquivo
```

### Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Suporte

- **Issues**: [GitHub Issues](https://github.com/your-username/bianca-ai/issues)
- **Documentação**: [Wiki](https://github.com/your-username/bianca-ai/wiki)
- **Email**: bianca@example.com

## 🙏 Agradecimentos

- OpenAI pela API e modelos
- Comunidade Python pelos recursos e bibliotecas
- Contribuidores do projeto

## 📊 Estatísticas

- **Versão Atual**: 1.0.0
- **Python**: 3.8+
- **Modelos Suportados**: 12
- **Dependências**: 3 principais

---

**BIANCA** - Simplificando o trabalho com IA! 🚀