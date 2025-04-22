import unittest
from git import Repo
from unittest.mock import patch, MagicMock
import os
import sys

# Adicione o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import git_automate 

class TestGitAutomation(unittest.TestCase):

    def setUp(self):
        self.repo_mock = MagicMock(spec=Repo)

    def test_executar_comando(self):
        with patch('git_automate.executar_comando', side_effect=self.executar_comando_mock) as mock_executar:
            resultado = git_automate.executar_comando("git status")
            self.assertEqual(resultado, 0)
            mock_executar.assert_called_once_with("git status")

    def test_menu_opcoes(self):
        with patch('builtins.input', side_effect=['1', 'sim']):
            git_automate.menu_opcoes(self.repo_mock)
            self.repo_mock.index.commit.assert_called_once()

        with patch('builtins.input', side_effect=['2', 'sim']):
            git_automate.menu_opcoes(self.repo_mock)
            self.repo_mock.git.push.assert_called_once()

        with patch('builtins.input', side_effect=['3', 'sim']):
            git_automate.menu_opcoes(self.repo_mock)
            self.repo_mock.git.pull.assert_called_once()

        with patch('builtins.input', side_effect=['4', 'sim']):
            git_automate.menu_opcoes(self.repo_mock)
            self.repo_mock.git.fetch.assert_called_once()
        
        with patch('builtins.input', side_effect=['0']):
            with patch('sys.exit') as mock_exit:
                git_automate.menu_opcoes(self.repo_mock)
                mock_exit.assert_called_once()
        
        def test_commit_arquivos(self):
            git_automate.commit_arquivos(commited=self.repo_mock)
            
            with patch('builtins.input', side_effect=['sim']):
                git_automate.commited(self.repo_mock)
                self.repo_mock.index.commit.assert_called_once()

            with patch('builtins.input', side_effect=['não']):
                with patch('builtins.input', return_value='teste de commit'):
                    git_automate.commited(self.repo_mock)
                    self.repo_mock.index.commit.assert_called_once_with()
            
            
            
        def test_principal(self):
            with patch('git_automate.selecionar_repositorio', return_value='/fake/path'):
                with patch('git_automate.abrir_repositorio', return_value=self.repo_mock):
                    git_automate.principal()
                    
                    
                    
            
            
            
            