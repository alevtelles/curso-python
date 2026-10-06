"""Capítulo 18: Escopo e armadilhas das funções.

Parte: Júnior.
Execute com: python cap18_escopo.py
"""


# === Escopo: onde um nome vale ===

mensagem = "global"


def externa():
    mensagem = "local da externa"

    def interna():
        print(mensagem)

    interna()
    print(mensagem)


externa()
print(mensagem)

contador = 0


def incrementar():
    global contador
    contador += 1


incrementar()
incrementar()
print(contador)


# === UnboundLocalError ===

total = 10


def quebrado():
    total += 1


try:
    quebrado()
except UnboundLocalError as erro:
    print(erro)


# === O valor padrão mutável ===

def adicionar(item, lista=[]):
    lista.append(item)
    return lista


print(adicionar(1))
print(adicionar(2))
print(adicionar.__defaults__)

def adicionar_correto(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista


print(adicionar_correto(1))
print(adicionar_correto(2))


# === Efeitos colaterais ===

def ordenar_no_lugar(lista):
    lista.sort()


def ordenada(lista):
    return sorted(lista)


original = [3, 1, 2]
nova = ordenada(original)
print(original, nova)
ordenar_no_lugar(original)
print(original)


# === Recursão ===

import sys


def fatorial(n):
    return 1 if n <= 1 else n * fatorial(n - 1)


print(fatorial(5))
print(sys.getrecursionlimit())


def sem_fim(n):
    return sem_fim(n + 1)


try:
    sem_fim(0)
except RecursionError:
    print("limite de recursão atingido")


# === Exercício: Corrija o bug do valor padrão ===

def registrar(evento, historico=None):
    if historico is None:
        historico = []
    historico.append(evento)
    return historico


assert registrar("a") == ["a"]
assert registrar("b") == ["b"]
assert registrar("c", ["x"]) == ["x", "c"]
print("ok")
