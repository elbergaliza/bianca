"""
BIANCA - Biblioteca de Inteligência Artificial para Novos Componentes e Aplicações

Uma biblioteca Python para facilitar o trabalho com modelos de IA da OpenAI,
incluindo cálculo de tokens, comparação de custos e configurações centralizadas.

Módulos principais:
- parametros: Configurações de modelos e API
- calcular_tokens: Cálculo de tokens e custos
- modelo: Classes para modelos de IA
- converter_audio_texto: Conversão de áudio para texto

Exemplo de uso:
    from bianca import CalculadoraTokens, obter_parametros
    
    # Calcular custos
    calc = CalculadoraTokens()
    custo = calc.calcular_custo('gpt-4o', 100, 50)
    
    # Obter configurações
    params = obter_parametros()
    modelos = params.listar_modelos_disponiveis()
"""

__version__ = "1.0.0"
__author__ = "BIANCA Team"
__email__ = "bianca@example.com"
__description__ = "Biblioteca de Inteligência Artificial para Novos Componentes e Aplicações"

# Importações principais para facilitar o uso
from .parametros import ParametrosIA, obter_parametros, ModeloConfig
from .calcular_tokens import CalculadoraTokens

# Importações opcionais (podem não estar disponíveis em todos os ambientes)
try:
    from .modelo import ModeloIA
except ImportError:
    ModeloIA = None

# try:
#     from .converter_audio_texto import ConversorAudioTexto
# except ImportError:
#     ConversorAudioTexto = None

# Lista de todas as classes e funções exportadas
__all__ = [
    # Versão e metadados
    '__version__',
    '__author__',
    '__email__',
    '__description__',

    # Classes principais
    'ParametrosIA',
    'ModeloConfig',
    'CalculadoraTokens',

    # Funções de conveniência
    'obter_parametros',

    # Classes opcionais
    'ModeloIA',
    # 'ConversorAudioTexto',
]

# Função de conveniência para obter informações do módulo


def obter_info():
    """Retorna informações sobre o módulo BIANCA"""
    return {
        'nome': 'BIANCA',
        'versao': __version__,
        'autor': __author__,
        'email': __email__,
        'descricao': __description__,
        'modulos_disponiveis': [
            'parametros',
            'calcular_tokens',
            'modelo' if ModeloIA else None,
            # 'converter_audio_texto' if ConversorAudioTexto else None,
        ],
        'classes_principais': [
            'ParametrosIA',
            'CalculadoraTokens',
            'ModeloIA' if ModeloIA else None,
            # 'ConversorAudioTexto' if ConversorAudioTexto else None,
        ]
    }

# Verificar se as dependências básicas estão disponíveis


def verificar_dependencias():
    """Verifica se as dependências básicas estão instaladas"""
    dependencias = {}

    try:
        import tiktoken
        dependencias['tiktoken'] = True
    except ImportError:
        dependencias['tiktoken'] = False

    try:
        import openai
        dependencias['openai'] = True
    except ImportError:
        dependencias['openai'] = False

    try:
        from dotenv import load_dotenv
        dependencias['python-dotenv'] = True
    except ImportError:
        dependencias['python-dotenv'] = False

    return dependencias

# Mensagem de boas-vindas quando o módulo é importado


def _mensagem_boas_vindas():
    """Exibe uma mensagem de boas-vindas (apenas na primeira importação)"""
    if not hasattr(_mensagem_boas_vindas, '_exibida'):
        print(
            f"BIANCA v{__version__} - Biblioteca de IA carregada com sucesso!")
        _mensagem_boas_vindas._exibida = True


# Executar mensagem de boas-vindas
_mensagem_boas_vindas()

# Função main para console script


def main():
    """Função principal para o console script bianca-info"""
    print("=" * 60)
    print("BIANCA - Biblioteca de IA")
    print("=" * 60)

    info = obter_info()
    print(f"Nome: {info['nome']}")
    print(f"Versão: {info['versao']}")
    print(f"Autor: {info['autor']}")
    print(f"Email: {info['email']}")
    print(f"Descrição: {info['descricao']}")

    print(f"\nMódulos disponíveis:")
    for modulo in info['modulos_disponiveis']:
        if modulo:
            print(f"  - {modulo}")

    print(f"\nClasses principais:")
    for classe in info['classes_principais']:
        if classe:
            print(f"  - {classe}")

    print(f"\nVerificando dependências:")
    dependencias = verificar_dependencias()
    for dep, status in dependencias.items():
        status_text = "✓" if status else "✗"
        print(f"  {status_text} {dep}")

    print("\n" + "=" * 60)
    print("Para mais informações, consulte: https://github.com/your-username/bianca-ai")
    print("=" * 60)


if __name__ == "__main__":
    main()
