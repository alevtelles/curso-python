"""Capítulo 38: Gerenciadores de contexto.

Parte: Intermediário.
Execute com: python cap38_context_managers.py
"""


# === O protocolo ===

import time


class Cronometro:
    def __enter__(self):
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, tipo_exc, valor_exc, traceback):
        self.duracao = time.perf_counter() - self.inicio
        return False


with Cronometro() as cron:
    sum(range(100_000))
print(cron.duracao >= 0)

class Ignorar:
    def __enter__(self):
        return self

    def __exit__(self, tipo_exc, valor_exc, traceback):
        print("saindo, erro:", tipo_exc.__name__ if tipo_exc else None)
        return tipo_exc is ZeroDivisionError


with Ignorar():
    1 / 0
print("continuou")


# === A forma curta: contextmanager ===

from contextlib import contextmanager


@contextmanager
def secao(titulo):
    print(f"[início] {titulo}")
    try:
        yield
    finally:
        print(f"[fim] {titulo}")


with secao("importação"):
    print("trabalhando")


# === Ferramentas prontas ===

from contextlib import suppress
from pathlib import Path
import tempfile

with suppress(FileNotFoundError):
    Path("nao_existe.txt").unlink()
print("sem erro")

with tempfile.TemporaryDirectory() as pasta:
    arquivo = Path(pasta) / "tmp.txt"
    arquivo.write_text("oi", encoding="utf-8")
    print(arquivo.exists())
print(Path(pasta).exists())


# === Exercício: Mudar de pasta e voltar ===

import os


@contextmanager
def mudar_pasta(destino):
    original = os.getcwd()
    os.chdir(destino)
    try:
        yield
    finally:
        os.chdir(original)


antes = os.getcwd()
with tempfile.TemporaryDirectory() as pasta:
    with mudar_pasta(pasta):
        assert os.getcwd() == os.path.realpath(pasta)
assert os.getcwd() == antes
print("ok")
