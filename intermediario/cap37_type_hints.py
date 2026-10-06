"""Capítulo 37: Type hints.

Parte: Intermediário.
Execute com: python cap37_type_hints.py
"""


# === Anotar parâmetros e retorno ===

def saudar(nome: str, vezes: int = 1) -> str:
    return (f"Olá, {nome}! " * vezes).strip()


print(saudar("Ana", 2))
print(saudar.__annotations__)
print(saudar(123))


# === Coleções, opcionais e uniões ===

def media(valores: list[float]) -> float:
    return sum(valores) / len(valores)


def buscar(config: dict[str, int], chave: str) -> int | None:
    return config.get(chave)


print(media([1.0, 2.0, 3.0]), buscar({"porta": 80}, "host"))


# === Aliases, funções e estruturas ===

from collections.abc import Callable
from typing import NamedTuple, TypedDict

type Predicado = Callable[[int], bool]


def filtrar(numeros: list[int], teste: Predicado) -> list[int]:
    return [n for n in numeros if teste(n)]


class Ponto(NamedTuple):
    x: int
    y: int


class Usuario(TypedDict):
    nome: str
    idade: int


u: Usuario = {"nome": "Ana", "idade": 30}
print(filtrar([1, 2, 3, 4], lambda n: n % 2 == 0))
print(Ponto(1, 2), u)


# === Exercício: Anote uma função de agrupamento ===

def agrupar_por_inicial(palavras: list[str]) -> dict[str, list[str]]:
    grupos: dict[str, list[str]] = {}
    for palavra in palavras:
        grupos.setdefault(palavra[0].lower(), []).append(palavra)
    return grupos


assert agrupar_por_inicial(["Ana", "aba", "Bia"]) == {"a": ["Ana", "aba"], "b": ["Bia"]}
print("ok")
