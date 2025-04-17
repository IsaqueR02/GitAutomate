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
        print("Fazendo push das mudanças para o remoto...")
        saida_push, erro_push = executar_comando("git push")
        if erro_push:
            print(f"Erro durante o push: {erro_push}")
            return
        print(saida_push)
        print("Mudanças enviadas com sucesso.")
    except Exception as e:
        git.Git().set_persistent_git_options(verbose=True)
        print(f"Erro durante o push: {e}")
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