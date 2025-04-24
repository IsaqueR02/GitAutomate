import logging
import os
import subprocess
import sys
from colorama import Fore, Style
from git import Repo, InvalidGitRepositoryError

from archives.repository_management import verificar_arquivos_modificados as status
from archives.repository_management import selecionar_repositorio
from archives.repository_management import change_repository_environment as repository
from archives.repository_crypted import get_credentials

from gitCommits.commitadd_management import adicionar_arquivos_especificos as add
from gitCommits.descommit_management import desfazer_commits as descommited
from gitCommits.commitadd_management import commit_workflow
from gitCommits.commitadd_management import gerar_mensagem_commit as commited

import branchsManager.changesManagement as changes_management
import branchsManager.doPush as doPush
import branchsManager.doPull as doPull

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        print("2. Adicionar mudanças")
        print("3. Commit")
        print("4. Push")
        print("5. Pull")
        print("6. Desfazer Últimos Commits")
        print("7. Mudar ambiente do repositório")
        print("8. Configurar credenciais")
        print("0. Sair")

        escolha = input("Digite sua escolha: ")
        if escolha == '1':
            status(repositorio)
        elif escolha == '2':
            add(repositorio)
        elif escolha == '3':
            commit_workflow(repositorio)
        elif escolha == '4':
            doPush.realizar_push(repositorio)
        elif escolha == '5':
            doPull.realizar_pull(repositorio)
        elif escolha == '6':
            descommited(repositorio)
        elif escolha == '7':
            repository(repositorio)
        elif escolha == '8':
            input("Digite a plataforma do repositório: ").lower()
            print("1. GitHub")
            print("2. Bitbucket")
            get_credentials
        elif escolha == '0':
            print("Saindo do programa.")
            break
        else:
            print("Escolha inválida, tente novamente.")
            
# Obter arquivos alterados
def commit_arquivos(repositorio):
    commit_workflow(repositorio)
    

def principal():
    try:
        repositorio = selecionar_repositorio()
        if not repositorio:
            print("Nenhum repositório selecionado. Encerrando o programa.")
            return
        
        logging.info(f"Repositório selecionado: {repositorio.working_tree_dir}")
    
        branch_selecionada = changes_management.verificar_branchs_remotas(repositorio)
        if not branch_selecionada:
            print("Nenhuma branch selecionada ou criada. Encerrando o script.")
            return

        menu_opcoes(repositorio)
    except Exception as e:
        logging.error(f"Erro ao selecionar o repositório: {e}")
        sys.exit(1)


if __name__ == "__main__":
    principal()
    
    ## Pontos a serem melhorados:
    # 2. Melhorar o gerenciamento de branches, permitindo ao usuário escolher a branch de destino.
    # 3. Incluir uma opção para desfazer o último commit, caso necessário.
    # 4. Melhorar o direncionamento do add, permitindo adicionar arquivos específicos ou diretórios.
    # 5. Melhorar a geração de mensagens de commit, talvez usando um modelo de IA ou análise de mudanças.
    # 7. Melhorar a interface do usuário, talvez inserindo mais interações ou estilo gráfico.
    # 9. Implementar um sistema de logs para registrar as ações realizadas pelo script.
    # 10. Inserir uma opção para visualizar o histórico de commits antes de fazer o push.
    # 11. Adicionar suporte para repositórios privados, incluindo autenticação.
    # 12. Melhorar a documentação do código e criar um README para o projeto.