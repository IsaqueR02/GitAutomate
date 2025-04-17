import subprocess
import os
import sys
from git import Repo
from git.exc import GitCommandError

import archives.repository_management as status
from gitCommits.descommit_management import desfazer_commits as descommited
from gitCommits.commitadd_management import gerar_mensagem_commit as commited
import branchsManager.changesManagement as changes_management
import branchsManager.doPush as doPush
import branchsManager.doPull as doPull

def executar_comando(comando):
    processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    saida, erro = processo.communicate()
    return saida.decode('utf-8'), erro.decode('utf-8'), processo.returncode

def menu_opcoes(repositorio):
    while True:
        print("\nEscolha uma opção:")
        print("1. Commit")
        print("2. Push")
        print("3. Pull")
        print("4. Desfazer Últimos Commits")
        print("0. Sair")
        
        escolha = input("Digite sua escolha: ")
        
        if escolha == '1':
            commited.gerar_mensagem_commit  # Chama sua função de commit
        elif escolha == '2':
            doPush.realizar_push(repositorio)  # Chama sua função de push
        elif escolha == '3':
            doPull.realizar_pull(repositorio)  # Chama sua função de pull
        elif escolha == '4':
            descommited.desfazer_commits(repositorio)  # Chama sua função para desfazer commits
        elif escolha == '0':
            print("Saindo do programa.")
            break
        else:
            print("Escolha inválida, tente novamente.")

def principal(repositorio):
    try:
        repositorio = Repo(os.getcwd())
    except Exception as e:
        print(f"Erro ao abrir o repositório git: {e}")
        print("Certifique-se de que este é um repositório git válido.")
        sys.exit(1)
        
    branch_selecionada = changes_management.verificar_branchs_remotas(repositorio)
    if not branch_selecionada:
        print("Nenhuma branch selecionada ou criada. Encerrando o script.")
        return

    if not status.verificar_arquivos_modificados(repositorio):
        print("Não há arquivos modificados para commit.")
        return

    # Git add .
    print("Executando 'git add .'")
    executar_comando("git add .")
    
    menu_opcoes(repositorio)

    # Obter arquivos alterados
    arquivos_alterados = status.obter_mudancas_arquivos(repositorio)
    if not arquivos_alterados:
        print("Não há mudanças para commit.")
        return

    # Gerar mensagem de commit
    mensagem_commit = commited.gerar_mensagem_commit(arquivos_alterados)

    # Mostrar mensagem de commit e pedir confirmação
    print(f"\nMensagem de commit escolhida: {mensagem_commit}")

    print(mensagem_commit)
    while True:
        confirmacao = input("Confirma esta mensagem de commit? (sim/não): ").lower()
        if confirmacao in ['sim', 's']:
            break
        elif confirmacao in ['não', 'nao', 'n']:
            mensagem_commit = input("Digite a nova mensagem de commit: ")
            break
        else:
            print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")

    # Commit das mudanças
    try:
        repositorio.index.commit(mensagem_commit)
        print("Mudanças commitadas com sucesso.")
    except GitCommandError as e:
        print(f"Erro durante o commit: {e}")
        return

    # Pedir confirmação antes do push
    entrada_usuario = input("\nVocê quer fazer push das mudanças? (sim/não): ").lower()
    if entrada_usuario in ['sim', 's', 'não', 'nao', 'n']:
        doPush.realizar_push(repositorio)

    if __name__ == "__main__":
        principal(repositorio)
    
    ## Pontos a serem melhorados:
    # 1. Adicionar tratamento de exceções para o caso de falhas no push ou pull.
    # 2. Melhorar o gerenciamento de branches, permitindo ao usuário escolher a branch de destino.
    # 3. Incluir uma opção para desfazer o último commit, caso necessário.
    # 4. Melhorar o direncionamento do add, permitindo adicionar arquivos específicos ou diretórios.
    # 5. Melhorar a geração de mensagens de commit, talvez usando um modelo de IA ou análise de mudanças.
    # 6. Adicionar suporte para múltiplos repositórios ou branches.
    # 7. Melhorar a interface do usuário, talvez inserindo mais interações ou estilo gráfico.
    # 8. Adicionar testes automatizados para garantir a funcionalidade do script.
    # 9. Implementar um sistema de logs para registrar as ações realizadas pelo script.
    # 10. Inserir uma opção para visualizar o histórico de commits antes de fazer o push.
    # 11. Adicionar suporte para repositórios privados, incluindo autenticação.
    # 12. Melhorar a documentação do código e criar um README para o projeto.