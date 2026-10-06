"""Capítulo 26: Classes e objetos.

Parte: Intermediário.
Execute com: python cap26_classes.py
"""


# === A classe é o molde, o objeto é a coisa ===

class Cachorro:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def latir(self):
        return f"{self.nome} diz: au au"


rex = Cachorro("Rex", 3)
mel = Cachorro("Mel", 5)
print(rex.nome, mel.nome)
print(rex.latir())


# === O que o self realmente é ===

print(Cachorro.latir(mel))
print(type(rex).__name__, isinstance(rex, Cachorro))


# === Uma representação que ajuda a depurar ===

class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Ponto(x={self.x}, y={self.y})"


p = Ponto(1, 2)
print(p)
print(vars(p))


# === Exercício: Uma conta bancária ===

class ContaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("o depósito deve ser positivo")
        self.saldo += valor

    def sacar(self, valor):
        if valor > self.saldo:
            raise ValueError("saldo insuficiente")
        self.saldo -= valor


conta = ContaBancaria("Ana", 100)
conta.depositar(50)
conta.sacar(30)
assert conta.saldo == 120
try:
    conta.sacar(500)
except ValueError:
    pass
else:
    raise AssertionError("deveria falhar")
print("ok")
