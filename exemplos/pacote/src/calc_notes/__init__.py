"""Pacote de exemplo do livro Python na Prática."""

from importlib.metadata import PackageNotFoundError, version

from calc_notes.operacoes import dividir, somar

try:
    __version__ = version("calc-notes")
except PackageNotFoundError:
    __version__ = "0+local"

__all__ = ["__version__", "dividir", "somar"]
