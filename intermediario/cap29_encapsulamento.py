"""Capítulo 29: Encapsulamento e @property.

Parte: Intermediário.
Execute com: python cap29_encapsulamento.py
"""


# === Convenções, não cadeados ===

class Conta:
    def __init__(self):
        self.titular = "Ana"
        self._saldo = 100
        self.__pin = 1234


conta = Conta()
print(conta.titular, conta._saldo)
try:
    conta.__pin
except AttributeError as erro:
    print(erro)
print(conta._Conta__pin)


# === property: validação sem mudar a interface ===

class ContaBancaria:
    def __init__(self, saldo=0):
        self._saldo = saldo

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if valor < 0:
            raise ValueError("saldo não pode ser negativo")
        self._saldo = valor


c = ContaBancaria(50)
c.saldo = 80
print(c.saldo)
try:
    c.saldo = -1
except ValueError as erro:
    print(erro)


# === Propriedades calculadas e somente leitura ===

class Retangulo:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    @property
    def area(self):
        return self.largura * self.altura


r = Retangulo(3, 4)
print(r.area)
try:
    r.area = 10
except AttributeError as erro:
    print(erro)


# === Exercício: Temperatura em Celsius e Fahrenheit ===

class Temperatura:
    def __init__(self, celsius=0):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, valor):
        if valor < -273.15:
            raise ValueError("abaixo do zero absoluto")
        self._celsius = valor

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, valor):
        self.celsius = (valor - 32) * 5 / 9


t = Temperatura(100)
assert t.fahrenheit == 212
t.fahrenheit = 32
assert t.celsius == 0
print("ok")
