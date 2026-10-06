"""Capítulo 43: MRO, super cooperativo e mixins.

Parte: Avançado.
Execute com: python cap43_mro_mixins.py
"""


# === A ordem que o Python segue ===

class Base:
    def ola(self):
        return ["Base"]


class Esquerda(Base):
    def ola(self):
        return ["Esquerda"] + super().ola()


class Direita(Base):
    def ola(self):
        return ["Direita"] + super().ola()


class Topo(Esquerda, Direita):
    def ola(self):
        return ["Topo"] + super().ola()


print(Topo().ola())
print([c.__name__ for c in Topo.__mro__])


# === __init__ cooperativo ===

class Nomeavel:
    def __init__(self, *, nome, **kwargs):
        super().__init__(**kwargs)
        self.nome = nome


class Datavel:
    def __init__(self, *, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data


class Evento(Nomeavel, Datavel):
    pass


e = Evento(nome="reunião", data="2026-10-06")
print(e.nome, e.data)


# === Mixins ===

import json


class JsonMixin:
    def para_json(self):
        return json.dumps(vars(self), ensure_ascii=False)


class ReprMixin:
    def __repr__(self):
        campos = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({campos})"


class Usuario(JsonMixin, ReprMixin):
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


u = Usuario("Ana", 30)
print(u)
print(u.para_json())


# === Ganchos de subclasse ===

class Comando:
    comandos = {}

    def __init_subclass__(cls, nome=None, **kwargs):
        super().__init_subclass__(**kwargs)
        Comando.comandos[nome or cls.__name__.lower()] = cls


class Listar(Comando, nome="ls"):
    pass


class Remover(Comando):
    pass


print(sorted(Comando.comandos))


# === Quando o MRO não fecha ===

class X:
    pass


class Y(X):
    pass


try:
    class Z(X, Y):
        pass
except TypeError as erro:
    print(erro)


# === Exercício: Registro de comandos ===

assert set(Comando.comandos) == {"ls", "remover"}
assert Comando.comandos["ls"] is Listar
print("ok")
