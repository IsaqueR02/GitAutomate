import os
import sys
from colorama import Fore, Style
from git import GitCommandError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from archives.repository_management import verificar_arquivos_modificados

def adicionar_arquivos_especificos(repositorio):
    arquivos_modificados = verificar_arquivos_modificados(repositorio)
    if not arquivos_modificados:
        print("Não há arquivos modificados para adicionar.")
        return
    
    arquivos_selecionados = []
    while True:
        print("1. Adicionar todos os arquivos modificados")
        print("2. Selecionar arquivos específicos")
        print("3. Adicionar um diretório")
        print("4. Voltar ao menu principal")
        escolha = input("Escolha uma opção (1-4): ")
        
        if escolha == '1':
            arquivos_selecionados = arquivos_modificados
            print("Todos os arquivos modificados foram adicionados.")
            break
        elif escolha == '2':
            arquivos_selecionados = selecionar_arquivos(arquivos_modificados)
            break
        elif escolha == '3':
            arquivos_selecionados = adicionar_diretorio(repositorio)
            break
        elif escolha == '4':
            print("Voltando ao menu principal.")
            return []
        else:
            print("Opção inválida. Tente novamente.")
            
    if arquivos_selecionados:
        for arquivo in arquivos_selecionados:
            repositorio.git.add(arquivo)
        print("Arquivos selecionados foram adicionados.")
    return arquivos_selecionados

def selecionar_arquivos(arquivos_modificados):
    arquivos_selecionados = []
    while arquivos_modificados:
        print("\nArquivos modificados:")
        for i, arquivo in enumerate(arquivos_modificados, 1):
            print(f"{i}. {arquivo}")
        
        escolha = input("\nDigite o número do arquivo para adicionar (ou 'q' para finalizar): ")
        if escolha.lower() == 'q':
            break
        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(arquivos_modificados):
                arquivo = arquivos_modificados.pop(indice)
                arquivos_selecionados.append(arquivo)
                print(f"Arquivo '{arquivo}' adicionado.")
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número ou 'q' para finalizar.")
    return arquivos_selecionados

def adicionar_diretorio(repositorio):
    diretorio = input("Digite o caminho do diretório que deseja adicionar: ")
    arquivos_adicionados = []
    if os.path.isdir(diretorio):
        for root, dirs, files in os.walk(diretorio):
            for file in files:
                file_path = os.path.join(root, file)
                repositorio.git.add(file_path)
                arquivos_adicionados.append(file_path)
                
        if arquivos_adicionados:
            print(f"Diretório '{diretorio}' adicionado.Arquivos incluídos:")
            for arquivo in arquivos_adicionados:
                print(f"- {arquivo}")
        else:
            print(f"Nenhum arquivo novo encontrado no diretório '{diretorio}'.")
    else:
        print("Caminho inválido ou diretório não encontrado.")
    
    return arquivos_adicionados

def gerar_mensagem_commit():
    # Lista de possíveis mensagens de commit
    mensagens_padrao = [
        "feat: Adição de novas funcionalidades.",
        "fix: Correção de bugs.",
        "refactor: Melhorias no código sem adição de funcionalidades ou correção de bugs.",
        "chore: Tarefas de manutenção e outras alterações que não afetam o código diretamente.",
        "perf: Melhorias de desempenho no código.",
        "test: Implementa testes automatizados.",
        "docs: Alterações na documentação."
        "style: Atualizações de formatação/código sem impacto no significado.",
        "ci: Ajustes relacionadas à configuração de integração contínua."
        "Modificado layout",
        "Implementado requisito",
        "Otimizado consultas de banco de dados"
    ]

    print("\nEscolha uma mensagem de commit ou digite uma nova:")
    for i, msg in enumerate(mensagens_padrao, 1):
        print(f"{i}. {msg}")
    print("0. Digitar uma mensagem personalizada")

    while True:
        escolha = input("\nDigite o número da opção desejada (0-12): ")
        if escolha.isdigit() and 0 <= int(escolha) <= len(mensagens_padrao):
            break
        print("Opção inválida. Por favor, escolha um número entre 0 e 12.")

    if escolha == '0':
        print("Gerando mensagem de commit detalhada:")
        tipo = input("Tipo de commit (feat/fix/docs/style/refactor/test/chore): ")
        escopo = input("Escopo (opcional): ")
        descricao = input("Descrição curta: ")
        corpo = input("Corpo do commit (opcional, pressione Enter para pular): ")
        
        mensagem = f"{tipo}"
        if escopo:
            mensagem += f"({escopo})"
        mensagem += f": {descricao}"
        if corpo:
            mensagem += f"\n\n{corpo}"
        return mensagem
    else:
        return mensagens_padrao[int(escolha) - 1]

# Commit das mudanças
def commit_workflow(repositorio):
    
    if not repositorio.is_dirty() and not repositorio.untracked_files:
        print("Não há mudanças para commit.")
        return
    
    arquivos_selecionados = adicionar_arquivos_especificos(repositorio)
    if not arquivos_selecionados:
        print("Nenhum arquivo selecionado para commit.")
        return

    mensagem_commit = gerar_mensagem_commit()
    
    while True:
        print(f"\nMensagem de commit escolhida: {mensagem_commit}")
        confirmacao = input("Confirma esta mensagem de commit? (sim/não): ").lower()
        if confirmacao in ['sim', 's']:
            try:
                repositorio.index.commit(mensagem_commit)
                print("Mudanças commitadas com sucesso.")
                break
            except GitCommandError as e:
                print(f"Erro durante o commit: {e}")
                return
        elif confirmacao in ['não', 'nao', 'n']:
            nova_mensagem = input("Deseja digitar uma nova mensagem de commit? (sim/não): ").lower()
            if nova_mensagem in ['sim', 's']:
                mensagem_commit = gerar_mensagem_commit()
            else:
                print("Commit cancelado.")
                return
        else:
            print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")

    if input("\nDeseja visualizar o histórico de commits? (sim/não): ").lower() in ['sim', 's']:
        visualizar_historico_commits(repositorio)

    if input("\nVocê quer fazer push das mudanças? (sim/não): ").lower() in ['sim', 's']:
        from branchsManager.doPush import realizar_push
        realizar_push(repositorio)

def visualizar_historico_commits(repositorio):
    while True:
        try:
            num_commits = int(input("Quantos commits recentes você quer ver? "))
            if num_commits > 0:
                break
            print("Por favor, insira um número positivo.")
        except ValueError:
            print("Por favor, insira um número válido.")
    
    commits = list(repositorio.iter_commits('HEAD', max_count=num_commits))
    
    print(Fore.CYAN + f"\nÚltimos {num_commits} commits:" + Style.RESET_ALL)
    for commit in commits:
        print(f"{Fore.YELLOW}{commit.hexsha[:7]}{Style.RESET_ALL} - {commit.summary}")
        print(f"Autor: {commit.author.name}")
        print(f"Data: {commit.committed_datetime}")
        print("-" * 40)