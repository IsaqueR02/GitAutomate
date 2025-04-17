import traceback
import git

def verificar_branchs_remotas(repositorio):
    try:
        # Verifica se há branches remotas
        print("Atualizando informações do repositório remoto...")
        repositorio.remotes.origin.fetch()
        branches_remotas = [ref.remote_head for ref in repositorio.remote().refs if not ref.remote_head.startswith('HEAD')]
        
        if not branches_remotas:
            print("Nenhuma branch remota encontrada.")
            criar_branch = input("Deseja criar uma nova branch? (sim/não): ").lower()
            if criar_branch in ['sim', 's']:
                nome_branch = input("Digite o nome da nova branch: ")
                repositorio.git.checkout('-b', nome_branch)
                print(f"Branch '{nome_branch}' criada com sucesso.")
            else:
                # Se não houver branches remotas e o usuário não quiser criar uma nova branch, o script termina
                print("Nenhuma branch remota encontrada e nenhuma nova branch criada.")
                return None

        print("Branches remotas encontradas:")
        for i, branch in enumerate(branches_remotas, 1):
            print(f"{i}. {branch}")

        # Pede ao usuário para selecionar uma branch
        while True:
            try:
                escolha = int(input("Selecione o número da branch desejada (ou 0 para criar uma nova): "))
                if 0 <= escolha <= len(branches_remotas):
                    break
                print("Escolha inválida. Por favor, tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        if escolha == 0:
            nome_branch = input("Digite o nome da nova branch: ")
            repositorio.git.checkout('-b', nome_branch)
            print(f"Nova branch '{nome_branch}' criada e selecionada.")
            return nome_branch
        else:
            branch_selecionada = branches_remotas[escolha - 1]
            repositorio.git.checkout(branch_selecionada)
            print(f"Branch '{branch_selecionada}' selecionada com sucesso.")
            
            # Verifica se a branch já existe localmente
            if branch_selecionada in [branch.name for branch in repositorio.branches]:
                repositorio.git.checkout(branch_selecionada)
                repositorio.git.pull('origin', branch_selecionada)
            else:
                # Cria a branch local rastreando a remota
                repositorio.git.checkout('-b', branch_selecionada, f'origin/{branch_selecionada}')
                
            print(f"Branch '{branch_selecionada}' selecionada e atualizada localmente.")
        
    except Exception as e:
        print(f"Erro ao verificar branches remotas: {e}")
        return False
    return True

def verificar_commits_remotos(repositorio):
    try:
        print("Iniciando verificação de commits remotos...")
        # Verifica se o repositório tem commits
        if len(list(repositorio.iter_commits())) == 0:
            print("O repositório não tem commits.")
            return False
        
        # Verifica se o repositório tem um remote configurado
        if 'origin' not in [remote.name for remote in repositorio.remotes]:
            print("Remote 'origin' não encontrado.")
            return False

        # Fetch das informações mais recentes do remote
        print("Atualizando informações do repositório remoto...")
        repositorio.remotes.origin.fetch()

        # Verifica o nome do branch atual
        try:
            branch_atual = repositorio.active_branch.name
        except Exception as e:
            print("Não foi possível determinar o branch atual.")
            return False

        # Verifica se o branch 'main' existe no remote
        if f'origin/{branch_atual}' not in repositorio.refs:
            print(f"O branch '{branch_atual}' não existe no remote.")
            return False

        print("Verificando commits remotos...")
        local_commit = repositorio.head.commit
        remote_commit = repositorio.refs[f'origin/{branch_atual}'].commit
        
        
        commits_atras = sum(1 for c in repositorio.iter_commits(f'{local_commit}..{remote_commit}'))
        print(f"Número de commits do remote: {commits_atras}")

        return commits_atras > 0
    except git.GitCommandError as e:
        print(f"Erro de comando Git ao verificar commits remotos: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado ao verificar commits remotos: {e}")
        print("Traceback completo:")
        traceback.print_exc()
        return False