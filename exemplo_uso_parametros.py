"""
Exemplo de uso do módulo de parâmetros de IA
Demonstra as principais funcionalidades implementadas
"""

from bianca.parametros import obter_parametros

try:
    import tiktoken
    TIKTOKEN_DISPONIVEL = True
except ImportError:
    TIKTOKEN_DISPONIVEL = False
    print("Aviso: tiktoken não está disponível. Algumas funcionalidades serão simuladas.")


def main():
    # Obtém a instância de parâmetros
    parametros = obter_parametros()

    print("=== BIANCA - Módulo de Parâmetros de IA ===\n")

    # 1. Listar todos os modelos disponíveis
    print("1. Modelos disponíveis:")
    modelos = parametros.listar_modelos()
    for nome, config in modelos.items():
        print(f"   - {nome}: {config.descricao}")
        print(
            f"     Preço entrada: ${config.preco_entrada_por_1k_tokens}/1k tokens")
        print(
            f"     Preço saída: ${config.preco_saida_por_1k_tokens}/1k tokens")
        print(f"     Limite: {config.limite_tokens} tokens")
        print()

    # 2. Calcular custos para diferentes modelos
    print("2. Cálculo de custos:")
    texto_exemplo = "Você é um categorizador de produtos. Categorize o seguinte produto: Camiseta de algodão orgânico."

    for nome_modelo in ['gpt-4', 'gpt-3.5-turbo']:
        try:
            if TIKTOKEN_DISPONIVEL:
                # Calcula tokens usando tiktoken
                codificador = tiktoken.encoding_for_model(nome_modelo)
                tokens_entrada = len(codificador.encode(texto_exemplo))
            else:
                # Simulação quando tiktoken não está disponível
                # Estimativa aproximada
                tokens_entrada = int(len(texto_exemplo.split()) * 1.3)

            tokens_saida = 50  # Estimativa de resposta

            custo = parametros.calcular_custo(
                nome_modelo, tokens_entrada, tokens_saida)
            print(f"   {nome_modelo}:")
            print(f"     Tokens entrada: {tokens_entrada}")
            print(f"     Tokens saída: {tokens_saida}")
            print(f"     Custo total: ${custo:.6f}")
            print()
        except Exception as e:
            print(f"   Erro ao calcular para {nome_modelo}: {e}")

    # 3. Verificar limites de tokens
    print("3. Verificação de limites:")
    tokens_teste = 10000
    for nome_modelo in ['gpt-4', 'gpt-3.5-turbo']:
        dentro_limite = parametros.verificar_limite_tokens(
            nome_modelo, tokens_teste)
        print(
            f"   {nome_modelo}: {tokens_teste} tokens {'✓' if dentro_limite else '✗'}")

    # 4. Obter configuração completa de um modelo
    print("\n4. Configuração completa do GPT-4:")
    config_completa = parametros.obter_configuracao_completa('gpt-4')
    for chave, valor in config_completa.items():
        print(f"   {chave}: {valor}")

    # 5. Comparar dois modelos
    print("\n5. Comparação entre modelos:")
    comparacao = parametros.comparar_modelos_configuracao(
        'gpt-4', 'gpt-3.5-turbo')
    print(
        f"   Modelo mais caro: {comparacao['comparacao']['modelo_mais_caro']}")
    print(
        f"   Modelo mais barato: {comparacao['comparacao']['modelo_mais_barato']}")
    print(
        f"   Diferença de preço entrada: ${comparacao['comparacao']['diferenca_preco_entrada']:.3f}")

    # 6. Configurações gerais
    print("\n6. Configurações gerais:")
    print(
        f"   Tempo de espera padrão: {parametros.obter_tempo_espera()} segundos")
    print(f"   Temperatura padrão: {parametros.obter_temperatura_padrao()}")
    print(f"   Max tokens padrão: {parametros.obter_max_tokens_padrao()}")
    print(
        f"   Chave API configurada: {'Sim' if parametros.obter_chave_api() else 'Não'}")

    # 7. Modificar configurações
    print("\n7. Modificando configurações:")
    parametros.definir_temperatura_padrao(0.5)
    parametros.definir_tempo_espera(60)
    print(f"   Nova temperatura: {parametros.obter_temperatura_padrao()}")
    print(
        f"   Novo tempo de espera: {parametros.obter_tempo_espera()} segundos")

    # 8. Exemplo de uso prático - simulação de requisição
    print("\n8. Simulação de requisição prática:")
    prompt = "Analise o sentimento do seguinte texto: 'Estou muito feliz com este produto!'"

    if TIKTOKEN_DISPONIVEL:
        codificador = tiktoken.encoding_for_model('gpt-3.5-turbo')
        tokens_prompt = len(codificador.encode(prompt))
    else:
        tokens_prompt = int(len(prompt.split()) * 1.3)

    tokens_resposta = 30  # Estimativa para análise de sentimento

    print(f"   Prompt: {prompt}")
    print(f"   Tokens entrada: {tokens_prompt}")
    print(f"   Tokens saída estimados: {tokens_resposta}")

    for modelo in ['gpt-4', 'gpt-3.5-turbo']:
        custo = parametros.calcular_custo(
            modelo, tokens_prompt, tokens_resposta)
        dentro_limite = parametros.verificar_limite_tokens(
            modelo, tokens_prompt, tokens_resposta)
        print(
            f"   {modelo}: Custo ${custo:.6f}, Limite {'✓' if dentro_limite else '✗'}")

    # 9. Demonstração de tratamento de erros
    print("\n9. Tratamento de erros:")
    try:
        parametros.calcular_custo('modelo-inexistente', 100, 50)
    except ValueError as e:
        print(f"   Erro capturado: {e}")

    try:
        parametros.definir_temperatura_padrao(3.0)  # Valor inválido
    except ValueError as e:
        print(f"   Erro capturado: {e}")

    # 10. Resumo final
    print("\n10. Resumo final:")
    print("   ✓ Módulo de parâmetros implementado com sucesso")
    print("   ✓ Configurações de modelos disponíveis")
    print("   ✓ Cálculo de custos funcional")
    print("   ✓ Verificação de limites implementada")
    print("   ✓ Comparação entre modelos disponível")
    print("   ✓ Configurações gerais gerenciáveis")
    print("   ✓ Tratamento de erros robusto")


if __name__ == "__main__":
    main()
