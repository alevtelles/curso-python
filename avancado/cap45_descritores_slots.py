"""Capítulo 45: Descritores, __slots__ e metaclasses.

Parte: Avançado.
Execute com: python cap45_descritores_slots.py
"""


# === O protocolo do descritor ===

class Positivo:
    def __set_name__(self, dono, nome):
        self.nome = "_" + nome

    def __get__(self, instancia, dono=None):
        if instancia is None:
            return self
        return getattr(instancia, self.nome)

    def __set__(self, instancia, valor):
        if valor <= 0:
            raise ValueError(f"{self.nome[1:]} deve ser positivo")
        setattr(instancia, self.nome, valor)


class Item:
    preco = Positivo()
    quantidade = Positivo()

    def __init__(self, preco, quantidade):
        self.preco = preco
        self.quantidade = quantidade


item = Item(10, 2)
print(item.preco * item.quantidade)
try:
    item.quantidade = 0
except ValueError as erro:
    print(erro)
print(type(Item.preco).__name__)

class A:
    def metodo(self):
        pass


bruto = A.__dict__["metodo"]
print(type(bruto).__name__, hasattr(bruto, "__get__"))


# === __slots__ ===

import tracemalloc


class Comum:
    def __init__(self, x, y):
        self.x, self.y = x, y


class Enxuta:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y


def medir(classe):
    tracemalloc.start()
    objetos = [classe(i, i) for i in range(50_000)]
    atual, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return atual


print(medir(Enxuta) < medir(Comum))
e = Enxuta(1, 2)
print(hasattr(e, "__dict__"))
try:
    e.z = 3
except AttributeError as erro:
    print(erro)


# === Metaclasses ===

Ponto = type("Ponto", (), {"x": 0, "ola": lambda self: "oi"})
print(Ponto().ola(), type(Ponto).__name__)


class Singleton(type):
    _instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instancias:
            Singleton._instancias[cls] = super().__call__(*args, **kwargs)
        return Singleton._instancias[cls]


class Configuracao(metaclass=Singleton):
    def __init__(self):
        self.valores = {}


print(Configuracao() is Configuracao())


# === Exercício: Um descritor de texto curto ===

class TextoCurto:
    def __init__(self, limite):
        self.limite = limite

    def __set_name__(self, dono, nome):
        self.nome = "_" + nome

    def __get__(self, instancia, dono=None):
        return self if instancia is None else getattr(instancia, self.nome)

    def __set__(self, instancia, valor):
        if len(valor) > self.limite:
            raise ValueError("texto longo demais")
        setattr(instancia, self.nome, valor)


class Perfil:
    bio = TextoCurto(5)


p = Perfil()
p.bio = "oi"
assert p.bio == "oi"
try:
    p.bio = "texto enorme"
except ValueError:
    pass
else:
    raise AssertionError("deveria falhar")
print("ok")
