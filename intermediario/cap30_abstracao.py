"""Capítulo 30: Abstração com ABC.

Parte: Intermediário.
Execute com: python cap30_abstracao.py
"""


# === O contrato ===

from abc import ABC, abstractmethod
import math


class Forma(ABC):
    @abstractmethod
    def area(self):
        ...

    def descrever(self):
        return f"{type(self).__name__} com área {self.area():.2f}"


class Circulo(Forma):
    def __init__(self, raio):
        self.raio = raio

    def area(self):
        return math.pi * self.raio ** 2


class Quadrado(Forma):
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return self.lado ** 2


for forma in (Circulo(1), Quadrado(2)):
    print(forma.descrever())


# === O erro vem cedo ===

try:
    Forma()
except TypeError as erro:
    print(erro)


class Incompleta(Forma):
    pass


try:
    Incompleta()
except TypeError as erro:
    print(erro)


# === Exercício: Notificadores ===

from abc import ABC, abstractmethod


class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensagem):
        ...


class Email(Notificador):
    def enviar(self, mensagem):
        return f"email: {mensagem}"


class SMS(Notificador):
    def enviar(self, mensagem):
        return f"sms: {mensagem}"


def avisar(notificadores, mensagem):
    return [n.enviar(mensagem) for n in notificadores]


assert avisar([Email(), SMS()], "oi") == ["email: oi", "sms: oi"]
print("ok")
