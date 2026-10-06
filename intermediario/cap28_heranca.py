"""Capítulo 28: Herança e polimorfismo.

Parte: Intermediário.
Execute com: python cap28_heranca.py
"""


# === Herdar e sobrescrever ===

class Animal:
    def __init__(self, nome):
        self.nome = nome

    def falar(self):
        return "..."

    def apresentar(self):
        return f"{self.nome} diz {self.falar()}"


class Cachorro(Animal):
    def falar(self):
        return "au"


class Gato(Animal):
    def falar(self):
        return "miau"


for animal in [Cachorro("Rex"), Gato("Mia"), Animal("Ser")]:
    print(animal.apresentar())


# === super(): reaproveitar o pai ===

class Funcionario:
    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def bonus(self):
        return self.salario * 0.1


class Gerente(Funcionario):
    def __init__(self, nome, salario, equipe):
        super().__init__(nome, salario)
        self.equipe = equipe

    def bonus(self):
        return super().bonus() + 100 * len(self.equipe)


g = Gerente("Ana", 5000, ["Bia", "Caio"])
print(g.bonus())


# === Hierarquias e a ordem de busca ===

class A:
    pass


class B(A):
    pass


class C(B):
    pass


print(issubclass(C, A), isinstance(C(), B))
print([k.__name__ for k in C.__mro__])


# === Duck typing ===

class Pato:
    def falar(self):
        return "quack"


class Robo:
    def falar(self):
        return "bip"


for coisa in (Pato(), Robo()):
    print(coisa.falar())


# === Composição antes de herança ===

class Motor:
    def ligar(self):
        return "motor ligado"


class Carro:
    def __init__(self):
        self.motor = Motor()

    def partir(self):
        return self.motor.ligar()


print(Carro().partir())


# === Exercício: Formas geométricas ===

import math


class Forma:
    def area(self):
        raise NotImplementedError


class Retangulo(Forma):
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def area(self):
        return self.largura * self.altura


class Circulo(Forma):
    def __init__(self, raio):
        self.raio = raio

    def area(self):
        return math.pi * self.raio ** 2


def area_total(formas):
    return sum(forma.area() for forma in formas)


assert area_total([Retangulo(2, 3), Retangulo(1, 1)]) == 7
assert round(Circulo(1).area(), 2) == 3.14
print("ok")
