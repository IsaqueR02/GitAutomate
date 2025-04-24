from colorama import Fore, Style
from git import GitCommandError

from archives.repository_crypted import get_credentials
from branchsManager.changesManagement import verificar_commits_remotos
from branchsManager.doPull import realizar_pull

def realizar_push(repositorio):
    opcional = input("Deseja fazer pull antes do push? (sim/não): ").lower()
    if opcional in ['sim', 's']:
        realizar_pull(repositorio)

    try:
        if repositorio.remote().url.startswith('https'):
            platform = 'github' if 'github.com' in repositorio.remote().url else 'bitbucket'
            username, token = get_credentials(platform)
            
            # Configura as credenciais temporariamente
            with repositorio.git.custom_environment(GIT_ASKPASS='echo', GIT_USERNAME=username, GIT_PASSWORD=token):
                repositorio.git.push()
            
            #remote_url = repositorio.remote().url
            #authenticated_url = remote_url.replace('https://', f'https://{username}:{token}@')
            #repositorio.git.push(authenticated_url)
        else:
            repositorio.git.push()
        print(Fore.GREEN + "Push realizado com sucesso." + Style.RESET_ALL)
    except GitCommandError as e:
        print(Fore.RED + f"Erro ao realizar push: {e}" + Style.RESET_ALL)
    else:
        print("Push realizado. Suas mudanças foram enviadas para o remoto.")

    if verificar_commits_remotos(repositorio) == True:
        print("Atenção: Há commits no remoto que não estão no seu repositório local.")
        print("É recomendado fazer pull antes de push para evitar conflitos.")
        continuar = input("Deseja ainda continuar com o push? (sim/não): ").lower()
        if continuar not in ['sim', 's']:
            pull = input("Deseja fazer pull das mudanças remotas? (sim/não): ").lower()
            if pull in ['sim', 's']:
                realizar_pull(repositorio)
                return