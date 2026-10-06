"""Capítulo 5: pipx: ferramentas de linha de comando isoladas.

Parte: Ambiente.
Execute com: python cap05_pipx.py
"""


# === Quais ferramentas estão no seu PATH ===

import shutil

for ferramenta in ["python3", "pipx", "uv", "poetry", "pyenv"]:
    caminho = shutil.which(ferramenta)
    situacao = f"instalado em {caminho}" if caminho else "não encontrado"
    print(f"{ferramenta:8} {situacao}")
