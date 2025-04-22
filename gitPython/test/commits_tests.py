import unittest
from git import Repo
from unittest.mock import patch, MagicMock
import os
import sys

# Adicione o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gitCommits import commitadd_management

class TestGitCommits(unittest.TestCase):

    def setUp(self):
        self.repo_mock = MagicMock(spec=Repo)
    
    def test_gerar_mensagem_commit(self):
        self.repo_mock.git.add = MagicMock()
        self.repo_mock.git.commit = MagicMock()
        self.repo_mock.git.diff.return_value = 'file1.txt\nfile2.txt'
        
        commitadd_management.gerar_mensagem_commit(['file1.txt', 'file2.txt'], self.repo_mock)
        
        self.repo_mock.git.add.assert_called_once_with(A=True)
        self.repo_mock.git.commit.assert_called_once()
        self.assertIn("Arquivos modificados:", self.repo_mock.git.diff.call_args[0][0])
    
    def test_commit_arquivos(self):
        self.repo_mock.index.commit = MagicMock()
        self.repo_mock.git.add = MagicMock()
        
        commitadd_management.commit_arquivos(self.repo_mock)
        
        self.repo_mock.git.add.assert_called_once_with(A=True)
        self.repo_mock.index.commit.assert_called_once()
    
    def test_selecionar_repositorio(self):
        with patch('os.listdir', return_value=['repo1', 'repo2']):
            with patch('os.path.isdir', return_value=True):
                with patch('os.path.exists', return_value=True):
                    result = commitadd_management.selecionar_repositorio()
                    self.assertIn(result, ['repo1', 'repo2'])

    def test_obter_mudancas_arquivos(self):
        self.repo_mock.git.diff.return_value = 'file1.txt\nfile2.txt'
        result = commitadd_management.obter_mudancas_arquivos(self.repo_mock)
        self.assertEqual(result, ['file1.txt', 'file2.txt'])
    
    def test_verificar_arquivos_modificados(self):
        self.repo_mock.git.diff.return_value = 'file1.txt\nfile2.txt'
        result = commitadd_management.verificar_arquivos_modificados(self.repo_mock)
        self.assertTrue(result)
        self.repo_mock.git.diff.return_value = ''
        
    def test_abrir_repositorio(self):
        with patch('git.Repo') as mock_repo:
            mock_repo.return_value = self.repo_mock
            result = commitadd_management.abrir_repositorio('/fake/path')
            self.assertIsNotNone(result)
    def test_desfazer_commits(self):
        self.repo_mock.git.reset = MagicMock()
        self.repo_mock.iter_commits = MagicMock(return_value=[MagicMock(hexsha='1234567', summary='Test commit')])
        
        with patch('builtins.input', side_effect=['sim', '1', 'sim']):
            commitadd_management.desfazer_commits(self.repo_mock)
            self.repo_mock.git.reset.assert_called_once_with('HEAD~1', soft=True)