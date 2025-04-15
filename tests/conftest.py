import os
import sys

# Adicionar o diretório raiz do projeto ao sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Obtém o caminho absoluto
sys.path.insert(0, ROOT)
