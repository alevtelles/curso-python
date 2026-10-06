"""Capítulo 49: Empacotamento e estrutura de projeto.

Parte: Avançado.
Execute com: python cap49_empacotamento.py
"""


# === Instalar em modo editável e usar ===

from importlib.metadata import PackageNotFoundError, version

try:
    print(version("pacote-que-nao-existe"))
except PackageNotFoundError as erro:
    print("não instalado:", erro)
