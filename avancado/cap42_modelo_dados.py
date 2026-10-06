"""Capítulo 42: O modelo de dados e os protocolos.

Parte: Avançado.
Execute com: python cap42_modelo_dados.py
"""


# === Uma sequência com dois métodos ===

import random
from collections import namedtuple

Carta = namedtuple("Carta", ["valor", "naipe"])


class Baralho:
    valores = [str(n) for n in range(2, 11)] + list("JQKA")
    naipes = ["paus", "ouros", "copas", "espadas"]

    def __init__(self):
        self._cartas = [Carta(v, n) for n in self.naipes for v in self.valores]

    def __len__(self):
        return len(self._cartas)

    def __getitem__(self, posicao):
        return self._cartas[posicao]


baralho = Baralho()
print(len(baralho), baralho[0], baralho[-1])
print(baralho[:3])
print(Carta("Q", "copas") in baralho)
print(random.choice(baralho) in baralho)


# === Ser, de fato, uma Sequence ===

from collections.abc import Container, Iterable, Sequence, Sized

print(isinstance(baralho, Sized), isinstance(baralho, Iterable), isinstance(baralho, Container))

class BaralhoSeq(Sequence):
    def __init__(self):
        self._cartas = Baralho()._cartas

    def __len__(self):
        return len(self._cartas)

    def __getitem__(self, posicao):
        return self._cartas[posicao]


b = BaralhoSeq()
print(isinstance(b, Sequence), Carta("A", "copas") in b)
print(b.index(Carta("3", "paus")), b.count(Carta("2", "paus")))


# === O contrato entre __eq__ e __hash__ ===

class Chave:
    def __init__(self, valor):
        self.valor = valor

    def __eq__(self, outro):
        return self.valor == outro.valor


try:
    {Chave(1)}
except TypeError as erro:
    print(erro)


class Mutavel:
    def __init__(self, v):
        self.v = v

    def __eq__(self, outro):
        return self.v == outro.v

    def __hash__(self):
        return hash(self.v)


m = Mutavel(1)
conjunto = {m}
m.v = 2
print(m in conjunto)


# === Acesso dinâmico a atributos ===

class Config:
    def __init__(self, **dados):
        self._dados = dados

    def __getattr__(self, nome):
        try:
            return self._dados[nome]
        except KeyError:
            raise AttributeError(nome) from None


c = Config(porta=8080)
print(c.porta, getattr(c, "host", "padrão"), hasattr(c, "porta"))


class Dinheiro:
    def __init__(self, centavos):
        self.centavos = centavos

    def __format__(self, formato):
        return format(self.centavos / 100, formato or ".2f")


print(f"{Dinheiro(1050)}", f"{Dinheiro(1050):.1f}")


# === Exercício: Um intervalo que se comporta como range ===

class Intervalo:
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim

    def __len__(self):
        return max(0, self.fim - self.inicio)

    def __getitem__(self, indice):
        if indice < 0:
            indice += len(self)
        if not 0 <= indice < len(self):
            raise IndexError(indice)
        return self.inicio + indice

    def __contains__(self, valor):
        return self.inicio <= valor < self.fim


assert list(Intervalo(3, 6)) == [3, 4, 5]
assert 4 in Intervalo(3, 6)
assert 6 not in Intervalo(3, 6)
assert Intervalo(3, 6)[-1] == 5
print("ok")
