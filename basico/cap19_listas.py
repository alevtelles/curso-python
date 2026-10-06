"""Capítulo 19: Listas.

Parte: Júnior.
Execute com: python cap19_listas.py
"""


# === Criar, acessar e fatiar ===

frutas = ["maçã", "banana", "manga"]
print(frutas[0], frutas[-1], frutas[0:2])
frutas[1] = "uva"
print(frutas)


# === Métodos principais ===

numeros = [3, 1, 4, 1, 5]
numeros.append(9)
numeros.insert(0, 0)
numeros.extend([2, 6])
print(numeros)
numeros.remove(1)
ultimo = numeros.pop()
print(numeros, ultimo)
print(numeros.index(4), numeros.count(1))

valores = [3, 1, 2]
print(sorted(valores))
print(valores)
resultado = valores.sort()
print(resultado, valores)
valores.sort(reverse=True)
print(valores)


# === Atribuir não é copiar ===

a = [1, 2, 3]
b = a
b.append(4)
print(a)
c = a.copy()
c.append(5)
print(a, c)

import copy

matriz = [[1, 2], [3, 4]]
rasa = matriz.copy()
rasa[0][0] = 99
print(matriz)
profunda = copy.deepcopy(matriz)
profunda[0][0] = 0
print(matriz, profunda)


# === Operações úteis ===

n = [4, 8, 2, 9]
print(len(n), min(n), max(n), sum(n))
print(n + [1], n * 2)
print(8 in n)
print(list(reversed(n)))
del n[0]
print(n)
n[1:3] = [0, 0, 0]
print(n)


# === Pilha e fila ===

from collections import deque

pilha = []
pilha.append("a")
pilha.append("b")
print(pilha.pop())

fila = deque(["x", "y", "z"])
fila.append("w")
print(fila.popleft(), list(fila))


# === Exercício: Segundo maior ===

def segundo_maior(numeros):
    unicos = sorted(set(numeros))
    return unicos[-2]


assert segundo_maior([4, 8, 2, 9, 1]) == 8
assert segundo_maior([5, 5, 3]) == 3
print("ok")


# === Exercício: A lista está ordenada? ===

def esta_ordenada(numeros):
    return numeros == sorted(numeros)


assert esta_ordenada([1, 3, 5])
assert not esta_ordenada([3, 1, 4])
assert esta_ordenada([])
print("ok")
