"""Capítulo 34: Iteradores e geradores.

Parte: Intermediário.
Execute com: python cap34_geradores.py
"""


# === Iterável e iterador ===

lista = [1, 2, 3]
iterador = iter(lista)
print(next(iterador), next(iterador), next(iterador))
try:
    next(iterador)
except StopIteration:
    print("acabou")

class Contagem:
    def __init__(self, limite):
        self.limite = limite
        self.atual = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.atual >= self.limite:
            raise StopIteration
        self.atual += 1
        return self.atual


print(list(Contagem(4)))


# === Funções geradoras com yield ===

def contagem(limite):
    atual = 1
    while atual <= limite:
        yield atual
        atual += 1


print(list(contagem(4)))
gerador = contagem(2)
print(next(gerador), next(gerador))


# === Preguiça é economia ===

import sys

lista = [n for n in range(100_000)]
gerador = (n for n in range(100_000))
print(sys.getsizeof(gerador) < sys.getsizeof(lista))
print(sum(gerador))

from itertools import islice


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print(list(islice(fibonacci(), 10)))


# === Pipelines ===

def sem_vazias(linhas):
    for linha in linhas:
        if linha.strip():
            yield linha


def numerar(linhas):
    for numero, linha in enumerate(linhas, start=1):
        yield f"{numero}: {linha}"


texto = ["primeira", "", "segunda", "  ", "terceira"]
print(list(numerar(sem_vazias(texto))))


# === Um gerador só pode ser percorrido uma vez ===

g = (n for n in range(3))
print(list(g), list(g))


# === Em lotes ===

from itertools import batched

print(list(batched("abcdefg", 3)))


# === Exercício: Dividir em lotes ===

from itertools import islice


def lotes(iteravel, tamanho):
    iterador = iter(iteravel)
    while True:
        lote = list(islice(iterador, tamanho))
        if not lote:
            return
        yield lote


assert list(lotes(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]
print("ok")
