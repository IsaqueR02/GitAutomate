from archives.repository_crypted import get_credentials
from git_automate import executar_comando

def realizar_pull(repositorio):
    try:
        print("Fazendo pull das mudanças do remoto...")
        platform = 'github' if 'github.com' in repositorio.remote().url else 'bitbucket'
        username, token = get_credentials(platform)
        remote_url = repositorio.remote().url
        authenticated_url = remote_url.replace('https://', f'https://{username}:{token}@')
        
        saida_pull, erro_pull, _ = executar_comando(f"git pull {authenticated_url}")
        if erro_pull:
            print(f"Erro durante o pull: {erro_pull}")
            return False
        print(saida_pull)
        print("Pull realizado. Mudanças do remoto integradas com sucesso.")
        return True
    except Exception as e:
        print(f"Erro durante o pull: {e}")
        return False