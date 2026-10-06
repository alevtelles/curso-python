"""Capítulo 20: Tuplas e conjuntos.

Parte: Júnior.
Execute com: python cap20_tuplas_conjuntos.py
"""


# === Tuplas ===

dias = ("seg", "ter", "qua")
print(dias[0], len(dias))
try:
    dias[0] = "dom"
except TypeError as erro:
    print(erro)

um = (1,)
nao_tupla = (1)
print(type(um), type(nao_tupla))

ponto = (3, 4)
x, y = ponto
primeiro, *resto = [10, 20, 30, 40]
print(x, y)
print(primeiro, resto)

from collections import namedtuple

Ponto = namedtuple("Ponto", ["x", "y"])
p = Ponto(3, 4)
print(p, p.x + p.y)

registro = ("ana", [1, 2])
registro[1].append(3)
print(registro)


# === Conjuntos ===

s = {1, 2, 2, 3, 3, 3}
print(s, len(s))
vazio = set()
print(type({}), type(vazio))
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b, a & b, a - b, a ^ b)
print(3 in a)

try:
    {[1, 2]}
except TypeError as erro:
    print(erro)

congelado = frozenset([1, 2])
print(congelado)


# === Exercício: Remover duplicatas preservando a ordem ===

def sem_duplicados(itens):
    vistos = set()
    resultado = []
    for item in itens:
        if item not in vistos:
            vistos.add(item)
            resultado.append(item)
    return resultado


assert sem_duplicados([3, 1, 3, 2, 1]) == [3, 1, 2]
print("ok")


# === Exercício: Itens em comum ===

def em_comum(a, b):
    return sorted(set(a) & set(b))


assert em_comum([1, 2, 3, 4], [3, 4, 5]) == [3, 4]
print("ok")
