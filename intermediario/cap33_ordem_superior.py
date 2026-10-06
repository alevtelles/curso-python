"""Capítulo 33: Funções de ordem superior.

Parte: Intermediário.
Execute com: python cap33_ordem_superior.py
"""


# === lambda e a chave de ordenação ===

pessoas = [("Ana", 31), ("Bia", 25), ("Caio", 31)]
print(sorted(pessoas, key=lambda p: p[1]))
print(sorted(pessoas, key=lambda p: (-p[1], p[0])))
print(max(pessoas, key=lambda p: p[1]))

from operator import itemgetter

produtos = [
    {"nome": "caneta", "preco": 3.5},
    {"nome": "caderno", "preco": 18.9},
    {"nome": "lápis", "preco": 1.2},
]
print([p["nome"] for p in sorted(produtos, key=itemgetter("preco"))])


# === map, filter e zip ===

numeros = [1, 2, 3, 4, 5]
dobrados = list(map(lambda n: n * 2, numeros))
pares = list(filter(lambda n: n % 2 == 0, numeros))
print(dobrados, pares)
print(type(map(str, numeros)).__name__)

nomes = ["Ana", "Bia", "Caio"]
notas = [9, 8]
print(list(zip(nomes, notas)))
try:
    list(zip(nomes, notas, strict=True))
except ValueError as erro:
    print(erro)


# === reduce e partial ===

from functools import partial, reduce
import operator


def potencia(base, expoente):
    return base ** expoente


quadrado = partial(potencia, expoente=2)
cubo = partial(potencia, expoente=3)
print(reduce(operator.mul, [1, 2, 3, 4], 1))
print(quadrado(5), cubo(2))


# === Exercício: Ordenar alunos por dois critérios ===

def ordenar_alunos(alunos):
    return sorted(alunos, key=lambda a: (-a["nota"], a["nome"]))


alunos = [
    {"nome": "Caio", "nota": 8},
    {"nome": "Ana", "nota": 9},
    {"nome": "Bia", "nota": 8},
]
assert [a["nome"] for a in ordenar_alunos(alunos)] == ["Ana", "Bia", "Caio"]
print("ok")
