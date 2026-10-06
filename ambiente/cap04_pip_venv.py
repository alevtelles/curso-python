"""Capítulo 4: pip e venv: dependências isoladas por projeto.

Parte: Ambiente.
Execute com: python cap04_pip_venv.py
"""


# === Como saber se você está dentro de um venv ===

import sys

dentro_de_venv = sys.prefix != sys.base_prefix
print("Dentro de um venv:", dentro_de_venv)
