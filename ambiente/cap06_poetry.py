"""Capítulo 6: Poetry: projetos, dependências e lockfile.

Parte: Ambiente.
Execute com: python cap06_poetry.py
"""


# === Ler o pyproject.toml pelo Python ===

import tomllib

texto = """
[project]
name = "meu-projeto"
dependencies = ["requests>=2.32"]
"""

dados = tomllib.loads(texto)
print(dados["project"]["name"])
print(dados["project"]["dependencies"])
