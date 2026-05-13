"""
Configuração global para os testes pytest.

Este arquivo é automaticamente descoberto pelo pytest e 
executado antes dos testes.
"""

import sys
import os

# Adiciona o diretório APIs ao path do Python para que os imports funcionem
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'APIs'))
