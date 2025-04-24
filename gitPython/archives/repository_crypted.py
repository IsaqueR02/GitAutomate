from colorama import Fore, Style
import keyring
import getpass

def get_credentials(platform):
    platform = 'github' if platform in ['1', 'github'] else 'bitbucket'
    
    
    username = keyring.get_password(platform, "username")
    token = keyring.get_password(platform, "token")
    
    if not username or not token:
        print(Fore.CYAN + f"\nConfigurando credenciais para {platform.upper()}" + Style.RESET_ALL)
        username = input(f"Digite seu nome de usuário do {platform}: ")
        token = getpass.getpass(f"Digite sua senha de acesso do {platform}: ")
        
        save = input("Deseja salvar essas credenciais para uso futuro? (s/n): ").lower()
        if save == 's':
            try:
                keyring.set_password(platform, "username", username)
                keyring.set_password(platform, "token", token)
                print(Fore.GREEN + "Credenciais salvas com sucesso!" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Erro ao salvar credenciais: {e}" + Style.RESET_ALL)
        else:
            print("Credenciais não foram salvas")
    else:
        print(Fore.GREEN + f"\nCredenciais encontradas para {platform}" + Style.RESET_ALL)
    
    return username, token