# Função para obter os arquivos alterados no repositório
def obter_mudancas_arquivos(repositorio):
    diff = repositorio.git.diff('HEAD', name_only=True)
    return diff.split('\n') if diff else []

def verificar_arquivos_modificados(repositorio):
    # Verifica se há arquivos modificados no repositório
    mudancas_arquivos = obter_mudancas_arquivos(repositorio)
    if not mudancas_arquivos:
        print("Nenhum arquivo modificado encontrado.")
        return False
    return True
