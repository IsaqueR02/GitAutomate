from colorama import Fore, Style
from git import Repo
from changesManagement import verificar_branchs_remotas

def listar_branches(repositorio):
    print(Fore.CYAN + "\nBranches disponíveis:" + Style.RESET_ALL)
    branches = [str(branch) for branch in repositorio.branches]
    if not branches:
        print(Fore.YELLOW + "Nenhuma branch encontrada." + Style.RESET_ALL)
        verificar_branchs_remotas(repositorio)
        return
    else:
        for i, branch in enumerate(branches, 1):
            print(f"{i}. {branch}")

def gerenciar_branches(repositorio):
    print(Fore.CYAN + "\nGerenciamento de Branches:" + Style.RESET_ALL)
    print("1. Listar branches")
    print("2. Criar nova branch")
    print("3. Mudar de branch")
    print("4. Deletar branch")
    
    escolha = input("Escolha uma opção: ")
    
    if escolha == '1':
        listar_branches(repositorio)
    elif escolha == '2':
        tipo_branch = input("Tipo de branch (task/feature/main): ").lower()
        nome_branch = input("Nome da nova branch: ")
        nome_completo = f"{tipo_branch}/{nome_branch}"
        repositorio.git.checkout('-b', nome_completo)
        print(Fore.GREEN + f"Branch '{nome_completo}' criada com sucesso." + Style.RESET_ALL)
    elif escolha == '3':
        branches = [str(branch) for branch in repositorio.branches]
        for i, branch in enumerate(branches, 1):
            print(f"{i}. {branch}")
        escolha_branch = int(input("Escolha o número da branch: ")) - 1
        repositorio.git.checkout(branches[escolha_branch])
        print(Fore.GREEN + f"Mudado para branch '{branches[escolha_branch]}'." + Style.RESET_ALL)
    elif escolha == '4':
        branches = [str(branch) for branch in repositorio.branches]
        for i, branch in enumerate(branches, 1):
            print(f"{i}. {branch}")
        escolha_branch = int(input("Escolha o número da branch para deletar: ")) - 1
        branch_to_delete = branches[escolha_branch]
        confirmacao = input(f"Tem certeza que deseja deletar '{branch_to_delete}'? (sim/não): ").lower()
        if confirmacao in ['sim', 's']:
            repositorio.git.branch('-D', branch_to_delete)
            print(Fore.GREEN + f"Branch '{branch_to_delete}' deletada com sucesso." + Style.RESET_ALL)