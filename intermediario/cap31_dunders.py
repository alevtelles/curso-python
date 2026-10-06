"""Capítulo 31: Métodos especiais.

Parte: Intermediário.
Execute com: python cap31_dunders.py
"""


# === Operadores e comparação ===

class Vetor:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vetor({self.x}, {self.y})"

    def __add__(self, outro):
        if not isinstance(outro, Vetor):
            return NotImplemented
        return Vetor(self.x + outro.x, self.y + outro.y)

    def __mul__(self, escalar):
        if not isinstance(escalar, (int, float)):
            return NotImplemented
        return Vetor(self.x * escalar, self.y * escalar)

    __rmul__ = __mul__

    def __eq__(self, outro):
        if not isinstance(outro, Vetor):
            return NotImplemented
        return (self.x, self.y) == (outro.x, outro.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __bool__(self):
        return bool(self.x or self.y)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


v1, v2 = Vetor(1, 2), Vetor(3, 4)
print(v1 + v2, v1 * 3, 3 * v1)
print(v1 == Vetor(1, 2), bool(Vetor(0, 0)), abs(v2))
print(len({v1, Vetor(1, 2)}))
try:
    v1 + 5
except TypeError as erro:
    print(erro)


# === Fazer o objeto virar um contêiner ===

class Playlist:
    def __init__(self, *musicas):
        self._musicas = list(musicas)

    def __len__(self):
        return len(self._musicas)

    def __getitem__(self, indice):
        return self._musicas[indice]

    def __contains__(self, musica):
        return musica in self._musicas


p = Playlist("a", "b", "c")
print(len(p), p[0], p[-1], "b" in p)
print(list(p), list(reversed(p)))


# === Objetos chamáveis ===

class Multiplicador:
    def __init__(self, fator):
        self.fator = fator

    def __call__(self, valor):
        return valor * self.fator


dobro = Multiplicador(2)
print(dobro(21), callable(dobro))


# === Ordenação sem escrever seis métodos ===

from functools import total_ordering


@total_ordering
class Versao:
    def __init__(self, texto):
        self.partes = tuple(int(p) for p in texto.split("."))

    def __eq__(self, outro):
        return self.partes == outro.partes

    def __lt__(self, outro):
        return self.partes < outro.partes

    def __repr__(self):
        return "Versao(" + ".".join(map(str, self.partes)) + ")"


print(sorted([Versao("1.10.0"), Versao("1.2.0"), Versao("1.9.5")]))
print(Versao("2.0") > Versao("1.9"))


# === Exercício: Uma classe Dinheiro ===

from functools import total_ordering


@total_ordering
class Dinheiro:
    def __init__(self, centavos):
        self.centavos = centavos

    def __add__(self, outro):
        if not isinstance(outro, Dinheiro):
            return NotImplemented
        return Dinheiro(self.centavos + outro.centavos)

    def __eq__(self, outro):
        if not isinstance(outro, Dinheiro):
            return NotImplemented
        return self.centavos == outro.centavos

    def __lt__(self, outro):
        if not isinstance(outro, Dinheiro):
            return NotImplemented
        return self.centavos < outro.centavos

    def __hash__(self):
        return hash(self.centavos)

    def __str__(self):
        reais, centavos = divmod(self.centavos, 100)
        return f"R$ {reais},{centavos:02d}"


assert str(Dinheiro(1050)) == "R$ 10,50"
assert Dinheiro(100) + Dinheiro(250) == Dinheiro(350)
assert Dinheiro(100) < Dinheiro(101)
print("ok")
