import logging
import os
import subprocess
import sys
from colorama import init, Fore, Style
from git import Repo
from git.exc import GitCommandError

import archives.repository_management as status
from gitCommits.descommit_management import desfazer_commits as descommited
from gitCommits.commitadd_management import gerar_mensagem_commit as commited
import branchsManager.changesManagement as changes_management
import branchsManager.doPush as doPush
import branchsManager.doPull as doPull

init(autoreset=True)

def executar_comando(comando):
    processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    saida, erro = processo.communicate()
    if processo.returncode != 0:
        print(f"Erro ao executar o comando '{comando}': {erro.decode('utf-8')}")
        return None
    else:
        print(f"Comando '{comando}' executado com sucesso.")
        print(saida.decode('utf-8'))
    return saida.decode('utf-8'), erro.decode('utf-8'), processo.returncode

def menu_opcoes(repositorio):

    while True:
        print("1. Verificar status")
        print("2. Adicionar mudanças (git add)")
        print("3. Commit")
        print("4. Push")
        print("5. Pull")
        print("6. Desfazer Últimos Commits")
        print("0. Sair")

        escolha = input("Digite sua escolha: ")
        if escolha == '1':
            status.verificar_arquivos_modificados(repositorio)
        elif escolha == '2':
            print("Executando 'git add .'")
            executar_comando("git add .")
        elif escolha == '3':
            commit_arquivos(repositorio)
        elif escolha == '4':
            doPush.realizar_push(repositorio)
        elif escolha == '5':
            doPull.realizar_pull(repositorio)
        elif escolha == '6':
            descommited(repositorio)
        elif escolha == '0':
            print("Saindo do programa.")
            break
        else:
            print("Escolha inválida, tente novamente.")
            
# Obter arquivos alterados
def commit_arquivos(repositorio):
    arquivos_alterados = status.obter_mudancas_arquivos(repositorio)
    if not arquivos_alterados:
        print("Não há mudanças para commit.")
        return
    
    # Gerar mensagem de commit
    mensagem_commit = commited(arquivos_alterados, repositorio)
    
    # Mostrar mensagem de commit e pedir confirmação
    print(f"\nMensagem de commit escolhida: {mensagem_commit}")
    while True:
        confirmacao = input("Confirma esta mensagem de commit? (sim/não): ").lower()
        if confirmacao in ['sim', 's']:
            break
        elif confirmacao in ['não', 'nao', 'n']:
            mensagem_commit = input("Digite a nova mensagem de commit: ")
            break
        else:
            print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")
        
        # Pedir confirmação antes do push
    if confirmacao in ['sim', 's']:
        entrada_usuario = input("\nVocê quer fazer push das mudanças? (sim/não): ").lower()
        if entrada_usuario in ['sim', 's', 'não', 'nao', 'n']:
            doPush.realizar_push(repositorio)
    
        # Commit das mudanças
        try:
            repositorio.index.commit(mensagem_commit)
            print("Mudanças commitadas com sucesso.")
        except GitCommandError as e:
            print(f"Erro durante o commit: {e}")

def principal(repositorio, ):
    try:
        repo_path = os.getcwd()
        repositorio = Repo(repo_path)
        logging.info(f"Repositório selecionado: {repo_path}")
    except Exception as e:
        logging.error(f"Erro ao abrir o repositório git: {e}")
        print(Fore.RED + f"Erro ao abrir o repositório git: {e}" + Style.RESET_ALL)
        print("Certifique-se de que este é um repositório git válido.")
        sys.exit(1)

    branch_selecionada = changes_management.verificar_branchs_remotas(repositorio)
    if not branch_selecionada:
        print("Nenhuma branch selecionada ou criada. Encerrando o script.")
        return

    menu_opcoes(repositorio)

if __name__ == "__main__":
    principal(Repo)
    
    ## Pontos a serem melhorados:
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