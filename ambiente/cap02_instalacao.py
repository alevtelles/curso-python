"""Capítulo 2: Instalando o Python no macOS, Windows e Linux.

Parte: Ambiente.
Execute com: python cap02_instalacao.py
"""


# === Conferir a instalação ===

import platform
import sys

print("Versão:", platform.python_version())
print("Implementação:", platform.python_implementation())
print("Executável:", sys.executable)
print("Sistema:", platform.system())
