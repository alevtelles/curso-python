"""Capítulo 44: Tipagem avançada.

Parte: Avançado.
Execute com: python cap44_tipagem_avancada.py
"""


# === Protocol: tipagem estrutural ===

from typing import Protocol, runtime_checkable


@runtime_checkable
class Fechavel(Protocol):
    def fechar(self) -> None: ...


class Arquivo:
    def fechar(self) -> None:
        print("arquivo fechado")


class Conexao:
    def fechar(self) -> None:
        print("conexão fechada")


def encerrar(recurso: Fechavel) -> None:
    recurso.fechar()


for recurso in (Arquivo(), Conexao()):
    encerrar(recurso)
print(isinstance(Arquivo(), Fechavel), isinstance(42, Fechavel))


# === Genéricos com a sintaxe do Python 3.12 ===

class Pilha[T]:
    def __init__(self) -> None:
        self._itens: list[T] = []

    def empilhar(self, item: T) -> None:
        self._itens.append(item)

    def desempilhar(self) -> T:
        return self._itens.pop()

    def __len__(self) -> int:
        return len(self._itens)


def primeiro[T](itens: list[T]) -> T:
    return itens[0]


def maximo[T: (int, float, str)](a: T, b: T) -> T:
    return a if a >= b else b


pilha = Pilha[int]()
pilha.empilhar(1)
pilha.empilhar(2)
print(pilha.desempilhar(), len(pilha), primeiro(["a", "b"]))
print(maximo(3, 7), maximo("a", "b"))


# === Literal, Final, TypedDict e Self ===

from typing import Final, Literal, NotRequired, Self, TypedDict

Modo = Literal["leitura", "escrita"]
LIMITE: Final = 3


class Opcoes(TypedDict):
    modo: Modo
    tentativas: NotRequired[int]


def abrir(opcoes: Opcoes) -> str:
    return f"{opcoes['modo']} com {opcoes.get('tentativas', LIMITE)} tentativas"


class Construtor:
    def __init__(self) -> None:
        self.partes: list[str] = []

    def adicionar(self, parte: str) -> Self:
        self.partes.append(parte)
        return self


print(abrir({"modo": "leitura"}))
print(Construtor().adicionar("a").adicionar("b").partes)


# === Sobrecarga e decoradores tipados ===

import functools
from collections.abc import Callable
from typing import overload


@overload
def dobrar(x: int) -> int: ...
@overload
def dobrar(x: str) -> str: ...
def dobrar(x):
    return x * 2


def registrar[**P, R](funcao: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(funcao)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"chamando {funcao.__name__}")
        return funcao(*args, **kwargs)

    return wrapper


@registrar
def somar(a: int, b: int) -> int:
    return a + b


print(dobrar(4), dobrar("ab"))
print(somar(1, 2))


# === Exercício: Um repositório genérico ===

class Repositorio[T]:
    def __init__(self) -> None:
        self._itens: dict[int, T] = {}

    def salvar(self, id_: int, item: T) -> None:
        self._itens[id_] = item

    def buscar(self, id_: int) -> T | None:
        return self._itens.get(id_)


repo = Repositorio[str]()
repo.salvar(1, "a")
assert repo.buscar(1) == "a"
assert repo.buscar(2) is None
print("ok")
