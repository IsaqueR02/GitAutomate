from git_automate import executar_comando

def realizar_pull():
    try:
        print("Fazendo pull das mudanças do remoto...")
        saida_pull, erro_pull = executar_comando("git pull")
        if erro_pull:
            print(f"Erro durante o pull: {erro_pull}")
            return
        print(saida_pull)
        print("Pull realizado. Mudanças do remoto integradas com sucesso.")
    except Exception as e:
        print(f"Erro durante o pull: {e}")