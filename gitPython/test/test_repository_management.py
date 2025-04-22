import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from git import Repo
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from archives import repository_management

class TestGitArchives(unittest.TestCase):

    def setUp(self):
        # Criar um repositório Git temporário para testes
        self.test_dir = tempfile.mkdtemp()
        self.local_repo_path = os.path.join(self.test_dir, 'local_repo')
        os.mkdir(self.local_repo_path)
        Repo.init(self.local_repo_path)

        # URL de um repositório remoto público para teste
        self.remote_repo_url = "https://github.com/octocat/Hello-World.git"

    def tearDown(self):
        # Limpar o diretório temporário após os testes
        shutil.rmtree(self.test_dir)

    def test_abrir_repositorio_local_sucesso(self):
        print("\nIniciando test_abrir_repositorio_local_sucesso")
        
        result = repository_management.abrir_repositorio(self.local_repo_path)
        
        print(f"Resultado: {result}")
        
        self.assertIsNotNone(result, "O resultado não deveria ser None")
        self.assertEqual(result.working_tree_dir, self.local_repo_path, "O caminho do repositório deveria ser igual ao fornecido")

        # Tentar fazer um fetch para verificar a conexão
        try:
            result.remotes.origin.fetch()
            print("Fetch bem-sucedido")
        except Exception as e:
            self.fail(f"Não foi possível fazer fetch do repositório remoto: {e}")

    def test_abrir_repositorio_caminho_invalido(self):
        print("\nIniciando test_abrir_repositorio_caminho_invalido")
        
        invalid_path = os.path.join(self.test_dir, 'non_existent')
        result = repository_management.abrir_repositorio(invalid_path)
        
        print(f"Resultado: {result}")
        self.assertIsNone(result, "O resultado deveria ser None para um caminho inválido")

    def test_abrir_repositorio_nao_git(self):
        print("\nIniciando test_abrir_repositorio_nao_git")
        
        non_git_path = self.test_dir  # Um diretório que existe, mas não é um repositório Git
        result = repository_management.abrir_repositorio(non_git_path)
        
        print(f"Resultado: {result}")
        self.assertIsNone(result, "O resultado deveria ser None para um diretório que não é um repositório Git")

if __name__ == '__main__':
    print("Iniciando testes")
    unittest.main(verbosity=2)