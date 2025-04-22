# Função para obter os arquivos alterados no repositório
import os
import sys
from colorama import Fore, Style
import git
from git import Repo


def obter_mudancas_arquivos(repositorio):
    diff = repositorio.git.diff('HEAD', name_only=True)
    return diff.split('\n') if diff else []

def verificar_arquivos_modificados(repositorio):
    # Verifica se há arquivos modificados no repositório
    mudancas_arquivos = obter_mudancas_arquivos(repositorio)
    if not mudancas_arquivos:
        print("Nenhum arquivo modificado encontrado.")
        return False
    else:
        print(f"Arquivos modificados: {', '.join(mudancas_arquivos)}")
        return True

def selecionar_repositorio():
    repos = [d for d in os.listdir() if os.path.isdir(d) and os.path.exists(os.path.join(d, '.git'))]
    if not repos:
        print(Fore.RED + "Nenhum repositório Git encontrado no diretório atual." + Style.RESET_ALL)
        sys.exit(1)
    
    print(Fore.CYAN + "Repositórios disponíveis:" + Style.RESET_ALL)
    for i, repo in enumerate(repos, 1):
        print(f"{i}. {repo}")
    
    while True:
        try:
            escolha = int(input("Selecione o número do repositório: "))
            if 1 <= escolha <= len(repos):
                return os.path.join(os.getcwd(), repos[escolha-1])
        except ValueError:
            pass
        print(Fore.RED + "Escolha inválida. Tente novamente." + Style.RESET_ALL)

def abrir_repositorio(caminho):
    try:
        repositorio = Repo(caminho)
        print(f"Repositório carregado em: {repositorio.working_tree_dir}")
        return repositorio
    except git.exc.InvalidGitRepositoryError:
        print("Certifique-se de que este é um repositório git válido.")
        return None
    except Exception as e:
        print(f"Erro ao abrir o repositório: {e}")
        return None