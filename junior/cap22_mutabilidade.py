"""Capítulo 22: Mutabilidade e identidade.

Parte: Júnior.
Execute com: python cap22_mutabilidade.py
"""


# === Nomes, objetos e id ===

a = [1, 2]
b = [1, 2]
c = a
print(a == b, a is b, a is c)
print(id(a) == id(c))


# === O que acontece nas funções ===

def anexar(lista):
    lista.append(99)


def reatribuir(lista):
    lista = [0]


dados = [1, 2]
anexar(dados)
print(dados)
reatribuir(dados)
print(dados)


# === A armadilha da matriz ===

errada = [[0] * 3] * 3
errada[0][0] = 1
print(errada)

certa = [[0] * 3 for _ in range(3)]
certa[0][0] = 1
print(certa)


# === Exercício: Copiar uma matriz de verdade ===

def copiar_matriz(matriz):
    return [linha.copy() for linha in matriz]


original = [[1, 2], [3, 4]]
copia = copiar_matriz(original)
copia[0][0] = 99
assert original == [[1, 2], [3, 4]]
assert copia == [[99, 2], [3, 4]]
print("ok")
