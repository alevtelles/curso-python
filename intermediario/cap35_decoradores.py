"""Capítulo 35: Closures e decoradores.

Parte: Intermediário.
Execute com: python cap35_decoradores.py
"""


# === Closures ===

def criar_contador():
    total = 0

    def contar():
        nonlocal total
        total += 1
        return total

    return contar


c = criar_contador()
print(c(), c(), c())
outro = criar_contador()
print(outro())


# === O decorador mais simples, e o erro que quase todo mundo comete ===

def decorador_ruim(funcao):
    def wrapper():
        return funcao()
    return wrapper


@decorador_ruim
def soma(a, b):
    return a + b


try:
    soma(2, 3)
except TypeError as erro:
    print(erro)

import functools


def registrar(funcao):
    @functools.wraps(funcao)
    def wrapper(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        print(f"{funcao.__name__}{args} -> {resultado}")
        return resultado
    return wrapper


@registrar
def multiplicar(a, b):
    """Multiplica dois números."""
    return a * b


multiplicar(3, 4)
print(multiplicar.__name__, multiplicar.__doc__)


# === Decoradores com parâmetros ===

def repetir(vezes):
    def decorador(funcao):
        @functools.wraps(funcao)
        def wrapper(*args, **kwargs):
            resultado = None
            for _ in range(vezes):
                resultado = funcao(*args, **kwargs)
            return resultado
        return wrapper
    return decorador


@repetir(3)
def avisar(texto):
    print(texto)


avisar("olá")


# === Um exemplo útil: tentar de novo ===

def tentar_novamente(tentativas):
    def decorador(funcao):
        @functools.wraps(funcao)
        def wrapper(*args, **kwargs):
            ultimo_erro = None
            for numero in range(1, tentativas + 1):
                try:
                    return funcao(*args, **kwargs)
                except ConnectionError as erro:
                    ultimo_erro = erro
                    print(f"tentativa {numero} falhou")
            raise ultimo_erro
        return wrapper
    return decorador


chamadas = {"total": 0}


@tentar_novamente(3)
def buscar():
    chamadas["total"] += 1
    if chamadas["total"] < 3:
        raise ConnectionError("rede fora")
    return "dados"


print(buscar())


# === Cache pronto ===

from functools import cache


@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(80))
print(fib.cache_info().hits > 0)


# === Exercício: Contar as chamadas de uma função ===

def contar_chamadas(funcao):
    @functools.wraps(funcao)
    def wrapper(*args, **kwargs):
        wrapper.chamadas += 1
        return funcao(*args, **kwargs)

    wrapper.chamadas = 0
    return wrapper


@contar_chamadas
def ola():
    return "oi"


ola()
ola()
assert ola.chamadas == 2
assert ola.__name__ == "ola"
print("ok")
