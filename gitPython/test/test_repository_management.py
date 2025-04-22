import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import git

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from archives import repository_management

class TestGitArchives(unittest.TestCase):

    def setUp(self):
        self.repo_mock = MagicMock()

    @patch('git.Repo')
    def test_abrir_repositorio_sucesso(self, mock_repo):
        mock_repo.return_value = self.repo_mock
        self.repo_mock.working_tree_dir = '/fake/path'
        
        with patch('builtins.print') as mock_print:
            result = repository_management.abrir_repositorio('/fake/path')
        
        self.assertIsNotNone(result)

    @patch('git.Repo')
    def test_abrir_repositorio_erro_invalido(self, mock_repo):
        mock_repo.side_effect = git.exc.InvalidGitRepositoryError()
        
        with patch('builtins.print') as mock_print:
            result = repository_management.abrir_repositorio('/fake/path')
        
        self.assertIsNone(result)

    @patch('git.Repo')
    def test_abrir_repositorio_erro_generico(self, mock_repo):
        mock_repo.side_effect = Exception("Erro genérico")
        
        with patch('builtins.print') as mock_print:
            result = repository_management.abrir_repositorio('/fake/path')
        
        self.assertIsNone(result)

    @patch('os.path.isdir', return_value=True)
    def test_obter_mudancas_arquivos_com_mudancas(self):
        self.repo_mock.git.diff.return_value = 'file1.txt\nfile2.txt'
        result = repository_management.obter_mudancas_arquivos(self.repo_mock)
        self.assertEqual(result, ['file1.txt', 'file2.txt'])

    @patch('os.path.isdir', return_value=False)
    def test_obter_mudancas_arquivos_sem_mudancas(self):
        self.repo_mock.git.diff.return_value = ''
        result = repository_management.obter_mudancas_arquivos(self.repo_mock)
        self.assertEqual(result, [])

    @patch('os.path.isdir', return_value=True)
    def test_verificar_arquivos_modificados_com_mudancas(self):
        with patch('archives.repository_management.obter_mudancas_arquivos', return_value=['file1.txt', 'file2.txt']):
            result = repository_management.verificar_arquivos_modificados(self.repo_mock)
        self.assertTrue(result)

    @patch('os.path.isdir', return_value=False)
    def test_verificar_arquivos_modificados_sem_mudancas(self):
        with patch('archives.repository_management.obter_mudancas_arquivos', return_value=[]):
            result = repository_management.verificar_arquivos_modificados(self.repo_mock)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()