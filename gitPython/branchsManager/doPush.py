from email.quoprimime import quote
from getpass import getpass
from colorama import Fore, Style
import git

from branchsManager.changesManagement import verificar_commits_remotos
from branchsManager.doPull import realizar_pull
import git_automate as executar_comando

def realizar_push(repositorio):
    opcional = input("Deseja fazer pull antes do push? (sim/não): ").lower()
    if opcional in ['sim', 's']:
        try:
            realizar_pull(repositorio)
        except Exception as e:
            print(f"Erro durante o pull: {e}")
        return

    try:
        if repositorio.remote().url.startswith('https'):
            username = input("Digite seu nome de usuário: ")
            password = getpass.getpass("Digite sua senha: ")
            encoded_password = quote(password)
            remote_url = repositorio.remote().url
            authenticated_url = remote_url.replace('https://', f'https://{username}:{encoded_password}@')
            repositorio.git.push(authenticated_url)
        else:
            repositorio.git.push()
        print(Fore.GREEN + "Push realizado com sucesso." + Style.RESET_ALL)
    except git.GitCommandError as e:
        print(Fore.RED + f"Erro ao realizar push: {e}" + Style.RESET_ALL)
    else:
        print("Push cancelado. Suas mudanças estão commitadas localmente.")

    if verificar_commits_remotos(repositorio) == True:
        print("Atenção: Há commits no remoto que não estão no seu repositório local.")
        print("É recomendado fazer pull antes de push para evitar conflitos.")
        continuar = input("Deseja ainda continuar com o push? (sim/não): ").lower()
        if continuar not in ['sim', 's']:
            pull = input("Deseja fazer pull das mudanças remotas? (sim/não): ").lower()
            if pull in ['sim', 's']:
                realizar_pull(repositorio)
                return