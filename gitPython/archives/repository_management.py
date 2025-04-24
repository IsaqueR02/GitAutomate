# Função para obter os arquivos alterados no repositório
import os
import sys
from colorama import Fore, Style
from git import Repo, InvalidGitRepositoryError
import git
from archives.repository_crypted import get_credentials

def obter_mudancas_arquivos(repositorio):
    diff = repositorio.git.diff('HEAD', name_only=True)
    return diff.split('\n') if diff else []

def verificar_arquivos_modificados(repositorio):
    # Verifica se há arquivos modificados no repositório
    arquivos_modificados = obter_mudancas_arquivos(repositorio)
    arquivos_nao_rastreados = repositorio.untracked_files
    todos_arquivos = (arquivos_modificados + arquivos_nao_rastreados)
    if not todos_arquivos:
        print(Fore.YELLOW + "Não há arquivos modificados ou novos para adicionar." + Style.RESET_ALL)
    elif arquivos_modificados:
        print(Fore.CYAN + "Arquivos modificados:" + Style.RESET_ALL)
        for arquivo in enumerate(arquivos_modificados):
            print(f"- {arquivo}")
    elif not arquivos_modificados:
        print(Fore.YELLOW + "Não há arquivos modificados para adicionar." + Style.RESET_ALL)
    
    elif arquivos_nao_rastreados:
        print(Fore.CYAN + "Arquivos novos:" + Style.RESET_ALL)
        for arquivo in enumerate(arquivos_nao_rastreados):
            print(f"- {arquivo}")
    elif not arquivos_nao_rastreados:
        print(Fore.YELLOW + "Não há arquivos novos para adicionar." + Style.RESET_ALL)
    
    return todos_arquivos

def adicionar_diretorio(repositorio):
    diretorio = input("Digite o caminho do diretório que deseja adicionar: ")
    if os.path.isdir(diretorio):
        repositorio.git.add(diretorio)
        print(f"Diretório '{diretorio}' adicionado.")
    else:
        print("Caminho inválido ou diretório não encontrado.")

def change_repository_environment(repositorio):
    print("\nEscolha o ambiente do repositório:")
    print("1. GitHub")
    print("2. Bitbucket")
    choice = input("Digite sua escolha (1 ou 2): ")
    
    if choice == '1':
        platform='github'
        new_remote = 'https://github.com/'
    elif choice == '2':
        platform='bitbucket'
        new_remote = 'https://bitbucket.org/'
    else:
        print("Escolha inválida.")
        return

    username, token = get_credentials(platform)
    if not username or not token:
        print("Credenciais não configuradas. Configure-as primeiro.")
        return
    
    repo_name = input("Digite o nome do repositório (usuario/repositorio): ")
    new_url = f"{new_remote}{repo_name}.git"

    try:
        repositorio.remote().set_url(new_url)
        print(f"Repositório alterado para {get_credentials(choice).capitalize()} com sucesso.")
        print(f"Nova URL: {new_url}")
    except Exception as e:
        print(f"Erro ao alterar o repositório: {e}")

def selecionar_repositorio():
    
    print("Diretório atual:", os.getcwd())
    
    # Tenta usar o repositório atual se for válido
    try:
        current_repo = Repo(os.getcwd())
        print(f"Repositório Git atual: {current_repo.working_tree_dir}")
        use_current = input("Deseja usar o repositório atual? (s/n): ").lower()
        if use_current == 's':
            return current_repo
    except InvalidGitRepositoryError:
        pass
    
    # Se não usar o atual, lista os repositórios disponíveis
    repos = []
    for d in os.listdir():
        try:
            repo_path = os.path.join(os.getcwd(), d)
            repo = Repo(repo_path)
            repos.append((d, repo))
        except InvalidGitRepositoryError:
            continue
        
    if not repos:
        print(Fore.RED + "Nenhum repositório Git encontrado no diretório atual." + Style.RESET_ALL)
        return None
    
    print(Fore.CYAN + "Repositórios disponíveis:" + Style.RESET_ALL)
    for i, (name, repo) in enumerate(repos, 1):
        print(f"{i}. {name} ({repo.working_tree_dir})")
    
    while True:
        try:
            escolha = int(input("Selecione o número do repositório: "))
            if 1 <= escolha <= len(repos):
                return repos[escolha-1][1]  # Retorna o objeto Repo
        except ValueError:
            pass
        print(Fore.RED + "Escolha inválida. Tente novamente." + Style.RESET_ALL)

def abrir_repositorio(caminho):
    try:
        if not os.path.exists(caminho):
            print(f"O caminho {caminho} não existe.")
            return None
        
        repositorio = Repo(caminho)
        
        if not repositorio.git_dir:
            print(f"O caminho {caminho} não é um repositório Git válido.")
            return None
        
        print(f"Repositório carregado com sucesso em: {repositorio.working_tree_dir}")
        return repositorio
    except git.exc.InvalidGitRepositoryError as e:
        print(f"Erro: Repositório inválido - {e}")
        return None
    except Exception as e:
        print(Fore.RED + f"Erro ao abrir o repositório: {e}" + Style.RESET_ALL)
        return None