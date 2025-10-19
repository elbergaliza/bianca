"""
Módulo de utilitários - BIANCA
Biblioteca de Inteligência Artificial para Novos Componentes e Aplicações

Este módulo contém funções utilitárias para operações com arquivos
e outras operações comuns do sistema.
"""

from pathlib import Path


def carregar_arquivo(caminho_arquivo: str, encoding: str = "utf-8") -> str:
    """
    Carrega o conteúdo de um arquivo de texto.

    Args:
        caminho_arquivo: Caminho completo ou relativo do arquivo a ser lido
        encoding: Codificação do arquivo (padrão: "utf-8")

    Returns:
        str: Conteúdo completo do arquivo como string

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        PermissionError: Se não houver permissão para ler o arquivo
        UnicodeDecodeError: Se houver erro na decodificação do arquivo

    Example:
        >>> conteudo = carrega_arquivo("./dados/avaliacoes-produto.txt")
        >>> print(conteudo)
    """
    try:
        with open(caminho_arquivo, "r", encoding=encoding) as f:
            dados_arquivo = f.read()
    except FileNotFoundError as e:
        e.add_note(f"Arquivo '{caminho_arquivo}' não encontrado.")
        raise e
    except PermissionError as e:
        e.add_note(f"Sem permissão para ler o arquivo '{caminho_arquivo}'.")
        raise e
    except UnicodeDecodeError as e:
        e.add_note(
            f"Erro ao decodificar o arquivo '{caminho_arquivo}' com encoding '{encoding}'."
        )
        raise e

    return dados_arquivo


def salvar_arquivo(
    caminho_arquivo: str,
    dados: str,
    encoding: str = "utf-8",
    criar_diretorios: bool = True
) -> None:
    """
    Salva dados em um arquivo de texto.

    Args:
        caminho_arquivo: Caminho completo ou relativo do arquivo a ser salvo
        dados: Conteúdo a ser gravado no arquivo
        encoding: Codificação do arquivo (padrão: "utf-8")
        criar_diretorios: Se True, cria diretórios automaticamente se não existirem

    Raises:
        PermissionError: Se não houver permissão para escrever o arquivo
        OSError: Se houver erro ao criar diretórios ou salvar o arquivo

    Example:
        >>> texto = "Resultado da análise..."
        >>> salvar_arquivo("./dados/resultado.txt", texto)
    """
    try:
        # Cria diretórios se necessário
        if criar_diretorios:
            Path(caminho_arquivo).parent.mkdir(parents=True, exist_ok=True)

        with open(caminho_arquivo, "w", encoding=encoding) as f:
            f.write(dados)
    except PermissionError as e:
        e.add_note(
            f"Sem permissão para salvar o arquivo '{caminho_arquivo}'."
        )
        raise e
    except OSError as e:
        e.add_note(
            f"Erro ao salvar o arquivo '{caminho_arquivo}'."
        )
        raise e


# Mantém nome antigo para compatibilidade com código existente
def salvando_arquivo(arquivo_produto: str, dados_arquivo: str) -> None:
    """
    DEPRECATED: Use salvar_arquivo() no lugar desta função.

    Salva dados em um arquivo de texto.
    Esta função está mantida apenas para compatibilidade com código legado.

    Args:
        arquivo_produto: Caminho do arquivo a ser salvo
        dados_arquivo: Conteúdo a ser gravado no arquivo

    Raises:
        Exception: Qualquer erro durante a operação de salvamento
    """
    try:
        with open(arquivo_produto, "w", encoding="utf-8") as f:
            f.write(dados_arquivo)
    except Exception as e:
        e.add_note(
            f"Problemas ao salvar o arquivo '{arquivo_produto}'."
        )
        raise e
