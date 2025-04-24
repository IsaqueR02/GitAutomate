import logging
import traceback
from colorama import Fore, Style
import git

def verificar_branchs_remotas(repositorio):
    try:
        # Verifica se há branches remotas
        print("\nAtualizando informações do repositório remoto...")
        repositorio.remotes.origin.fetch()
        
        branches_locais = [branch.name for branch in repositorio.branches]
        branches_remotas = [ref.remote_head for ref in repositorio.remote().refs if not ref.remote_head.startswith('HEAD')]
        
        if not branches_remotas:
            print(Fore.YELLOW + "Nenhuma branch remota encontrada." + Style.RESET_ALL)
            criar_branch = input("Deseja criar uma nova branch? (sim/não): ").lower()
            if criar_branch in ['sim', 's']:
                tipo_branch = input("Tipo de branch (task/feature/main): ").lower()
                nome_branch = input("Digite o nome da nova branch: ")
                nome_completo = f"{tipo_branch}/{nome_branch}"
                repositorio.git.checkout('-b', nome_completo)
                print(Fore.GREEN + f"Branch '{nome_completo}' criada com sucesso." + Style.RESET_ALL)
                logging.info(f"Nova branch criada: {nome_completo}")
                return nome_completo

        todas_branches = list(set(branches_locais + branches_remotas))
        todas_branches.sort()

        print("\nBranches disponíveis:")
        for i, branch in enumerate(todas_branches, 1):
            remote = "- R" if branch in branches_remotas else " "
            print(f"{i}. {branch} {remote}")

        # Pede ao usuário para selecionar uma branch
        while True:
            try:
                escolha = int(input("Selecione o número da branch desejada (ou 0 para criar uma nova): "))
                if 0 <= escolha <= len(todas_branches):
                    break
                print("Escolha inválida. Por favor, tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        if escolha == 0:
            create_new_branch(repositorio)
        else:
            branch_selecionada = todas_branches[escolha - 1]
            return checkout_e_atualizar_branch(repositorio, branch_selecionada, branches_locais, branches_remotas)
        
    except Exception as e:
        print(f"Erro ao verificar branches remotas: {e}")
        return False

def checkout_e_atualizar_branch(repositorio, branch, branches_locais, branches_remotas):
    if branch in branches_locais:
        repositorio.git.checkout(branch)
        if branch in branches_remotas:
            print(f"Branch '{branch}' existe localmente e remotamente.")
            if input("Deseja atualizar a branch local com a remota? (s/n): ").lower() == 's':
                repositorio.git.pull('origin', branch)
        else:
            print(f"Branch '{branch}' existe apenas localmente.")
            if input("Deseja fazer push desta branch para o remoto? (s/n): ").lower() == 's':
                repositorio.git.push('--set-upstream', 'origin', branch)
    elif branch in branches_remotas:
        print(f"Branch '{branch}' existe apenas remotamente.")
        repositorio.git.checkout('-b', branch, f'origin/{branch}')
        print(f"Branch '{branch}' criada localmente e configurada para rastrear a branch remota.")
    else:
        print(f"Erro: A branch '{branch}' não foi encontrada localmente nem remotamente.")
        return False
    
    print(f"Branch '{branch}' selecionada e atualizada.")
    return branch

def create_new_branch(repositorio):
    nome_branch = input("Digite o nome da nova branch: ")
    repositorio.git.checkout('-b', nome_branch)
    print(f"Nova branch '{nome_branch}' criada e selecionada.")
    return nome_branch

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