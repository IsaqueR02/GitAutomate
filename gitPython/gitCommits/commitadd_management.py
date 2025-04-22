from colorama import Fore, Style


from gitPython.archives.repository_management import obter_mudancas_arquivos


def gerar_mensagem_commit(mudancas_arquivos, repositorio):
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

    # Adicionar arquivos específicos ou todos
    while True:
        adicionar_todos = input("Adicionar todos os arquivos modificados? (sim/não): ").lower()
        if adicionar_todos in ['sim', 's']:
            repositorio.git.add(A=True)
            break
        elif adicionar_todos in ['não', 'nao', 'n']:
            arquivos_modificados = obter_mudancas_arquivos(repositorio)
            for i, arquivo in enumerate(arquivos_modificados, 1):
                print(f"{i}. {arquivo}")
            arquivos_selecionados = input("Digite os números dos arquivos a adicionar (separados por espaço): ")
            for num in arquivos_selecionados.split():
                if num.isdigit() and 1 <= int(num) <= len(arquivos_modificados):
                    repositorio.git.add(arquivos_modificados[int(num)-1])
            break
        else:
            print(Fore.RED + "Resposta inválida. Por favor, responda 'sim' ou 'não'." + Style.RESET_ALL)

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
        print("Gerando mensagem de commit detalhada:")
        tipo = input("Tipo de commit (feat/fix/docs/style/refactor/test/chore): ")
        escopo = input("Escopo (opcional): ")
        descricao = input("Descrição curta: ")
        corpo = input("Corpo do commit (opcional, pressione Enter para pular): ")
        
        mensagem = f"{tipo}"
        if escopo:
            mensagem += f"({escopo})"
        mensagem += f": {descricao}"
        if corpo:
            mensagem += f"\n\n{corpo}"
    #if escolha == '0':
    #    return input("Digite sua mensagem de commit personalizada: ")
    else:
        return mensagens_padrao[int(escolha) - 1]

def visualizar_historico_commits(repositorio):
    num_commits = int(input("Quantos commits recentes você quer ver? "))
    commits = list(repositorio.iter_commits('HEAD', max_count=num_commits))
    
    print(Fore.CYAN + f"\nÚltimos {num_commits} commits:" + Style.RESET_ALL)
    for commit in commits:
        print(f"{Fore.YELLOW}{commit.hexsha[:7]}{Style.RESET_ALL} - {commit.summary}")
        print(f"Autor: {commit.author.name}")
        print(f"Data: {commit.committed_datetime}")
        print("-" * 40)