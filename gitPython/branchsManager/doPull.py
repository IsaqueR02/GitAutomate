import keyring
from git_automate import executar_comando

def get_credentials():
    username = keyring.get_password("bitbucket", "username")
    token = keyring.get_password("bitbucket", "token")
    
    if not username or not token:
        username = input("Digite seu nome de usuário do Bitbucket: ")
        token = input("Digite seu token de acesso do Bitbucket: ")
        
        keyring.set_password("bitbucket", "username", username)
        keyring.set_password("bitbucket", "token", token)
    
    return username, token

def realizar_pull(repositorio):
    try:
        print("Fazendo pull das mudanças do remoto...")
        username, token = get_credentials()
        remote_url = repositorio.remote().url
        authenticated_url = remote_url.replace('https://', f'https://{username}:{token}@')
        
        
        print("Fazendo pull das mudanças do remoto...")
        saida_pull, erro_pull = executar_comando("git pull")
        if erro_pull:
            print(f"Erro durante o pull: {erro_pull}")
            return False
        print(saida_pull)
        print("Pull realizado. Mudanças do remoto integradas com sucesso.")
        return True
    except Exception as e:
        print(f"Erro durante o pull: {e}")
        return False