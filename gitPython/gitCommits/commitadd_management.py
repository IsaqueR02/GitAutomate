def gerar_mensagem_commit(mudancas_arquivos):
    # Lista de possíveis mensagens de commit
    mensagens_padrao = [
        "Desenvolvida nova funcionalidade",
        "Corrigido bug",
        "Atualizado documentação",
        "Refatorado código",
        "Melhorado desempenho",
        "Adicionado testes",
        "Atualizado dependências",
        "Modificado layout",
        "Implementado requisito",
        "Otimizado consultas de banco de dados"
    ]

    print("\nArquivos modificados:")
    for arquivo in mudancas_arquivos:
        if arquivo:
            print(f"- {arquivo}")

    print("\nEscolha uma mensagem de commit ou digite uma nova:")
    for i, msg in enumerate(mensagens_padrao, 1):
        print(f"{i}. {msg}")
    print("0. Digitar uma mensagem personalizada")

    while True:
        escolha = input("\nDigite o número da opção desejada (0-10): ")
        if escolha.isdigit() and 0 <= int(escolha) <= len(mensagens_padrao):
            break
        print("Opção inválida. Por favor, escolha um número entre 0 e 10.")

    if escolha == '0':
        return input("Digite sua mensagem de commit personalizada: ")
    else:
        return mensagens_padrao[int(escolha) - 1]
