import git

def desfazer_commits(repositorio):
    confirmacao = input("Você deseja desfazer os últimos commits? (sim/não): ").lower()
    if confirmacao not in ['sim', 's']:
        return None
    try:
        # Listar os últimos commits
        commits = list(repositorio.iter_commits(max_count=10))
        if not commits:
            print("Não há commits para desfazer.")
            return False

        print("Últimos commits:")
        for i, commit in enumerate(commits, 1):
            print(f"{i}. {commit.hexsha[:7]} - {commit.summary}")

        # Pedir ao usuário para escolher quantos commits desfazer
        while True:
            try:
                num_commits = int(input("Quantos commits você deseja desfazer? (0 para cancelar): "))
                if 0 <= num_commits <= len(commits):
                    break
                print("Número inválido. Por favor, tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        if num_commits == 0:
            print("Operação cancelada.")
            return False

        # Perguntar se o usuário quer manter as alterações
        manter_alteracoes = input("Deseja manter as alterações dos commits desfeitos? (sim/não): ").lower() in ['sim', 's']

        # Desfazer os commits
        if manter_alteracoes:
            repositorio.git.reset(f"HEAD~{num_commits}", soft=True)
            print(f"Os últimos {num_commits} commits foram desfeitos. As alterações foram mantidas no diretório de trabalho.")
        else:
            repositorio.git.reset(f"HEAD~{num_commits}", hard=True)
            print(f"Os últimos {num_commits} commits foram desfeitos e as alterações foram descartadas.")

    except git.GitCommandError as e:
        print(f"Erro ao desfazer commits: {e}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False
