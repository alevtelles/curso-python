"""Capítulo 36: dataclasses.

Parte: Intermediário.
Execute com: python cap36_dataclasses.py
"""


# === O básico ===

from dataclasses import dataclass, field, asdict, replace


@dataclass
class Produto:
    nome: str
    preco: float
    tags: list[str] = field(default_factory=list)


p = Produto("caneta", 3.5)
print(p)
print(p == Produto("caneta", 3.5))


# === O valor padrão mutável, outra vez ===

try:
    @dataclass
    class Ruim:
        itens: list = []
except ValueError as erro:
    print(erro)


# === Imutável, ordenável e econômica ===

@dataclass(frozen=True, order=True, slots=True)
class Versao:
    major: int
    minor: int = 0


v1, v2 = Versao(1, 2), Versao(1, 10)
print(v1 < v2, sorted([v2, v1]))
try:
    v1.major = 5
except Exception as erro:
    print(type(erro).__name__)


# === Validação, cópia e conversão ===

@dataclass
class Pedido:
    cliente: str
    itens: list[tuple[str, float]] = field(default_factory=list)

    def __post_init__(self):
        if not self.cliente:
            raise ValueError("cliente é obrigatório")

    @property
    def total(self):
        return sum(preco for _, preco in self.itens)


pedido = Pedido("Ana", [("caneta", 3.5), ("caderno", 18.9)])
print(round(pedido.total, 2))
print(asdict(pedido))
copia = replace(pedido, cliente="Bia")
print(copia.cliente, pedido.cliente)


# === Exercício: Um livro validado ===

@dataclass
class Livro:
    titulo: str
    paginas: int

    def __post_init__(self):
        if self.paginas <= 0:
            raise ValueError("páginas devem ser positivas")


assert Livro("Dom Casmurro", 256).paginas == 256
try:
    Livro("Vazio", 0)
except ValueError:
    pass
else:
    raise AssertionError("deveria falhar")
print("ok")
