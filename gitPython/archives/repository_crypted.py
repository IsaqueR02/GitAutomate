import os
from colorama import Fore, Style
import getpass

def get_credentials(platform):
    # Implemente a lógica para obter o token de acesso pessoal
    # Você pode armazená-lo em um arquivo de configuração seguro ou usar variáveis de ambiente
    if platform in ['1', 'github']:
        platform = 'github'
        #return os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN')
    elif platform in ['2', 'bitbucket']:
        platform = 'bitbucket'
        #return os.getenv('BITBUCKET_USERNAME'), os.getenv('BITBUCKET_TOKEN')
    else:
        raise ValueError("Plataforma não suportada")
    
    username = os.getenv(f'{platform.upper()}_USERNAME')
    token = os.getenv(f'{platform.upper()}_TOKEN')
    
    if not username or not token:
        print(Fore.CYAN + f"\nConfigurando credenciais para {platform.upper()}" + Style.RESET_ALL)
        username = input(f"Digite seu nome de usuário do {platform}: ")
        token = getpass.getpass(f"Digite sua senha de acesso do {platform}: ")
        
        save = input("Deseja salvar essas credenciais para uso futuro? (s/n): ").lower()
        if save == 's':
            try:
                os.environ[f'{platform.upper()}_USERNAME'] = username
                os.environ[f'{platform.upper()}_TOKEN'] = token
                print(Fore.GREEN + "Credenciais salvas com sucesso!" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Erro ao salvar credenciais: {e}" + Style.RESET_ALL)
        else:
            print("Credenciais não foram salvas")
    else:
        print(Fore.GREEN + f"\nCredenciais encontradas para {platform}" + Style.RESET_ALL)
    
    return username, token