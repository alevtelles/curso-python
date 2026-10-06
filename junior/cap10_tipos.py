"""Capítulo 10: Tipos de dados.

Parte: Júnior.
Execute com: python cap10_tipos.py
"""


# === Os tipos básicos ===

print(type(42), type(3.14), type(3 + 4j), type("oi"), type(True), type(None))


# === Inteiros sem limite, decimais com limite ===

print(2 ** 100)
print(1_000_000)

from decimal import Decimal
import math

print(0.1 + 0.2)
print(math.isclose(0.1 + 0.2, 0.3))
print(Decimal("0.1") + Decimal("0.2"))


# === bool é um tipo de int ===

print(True + True)
print(isinstance(True, int))


# === None ===

resultado = None
print(resultado is None)


# === Exercício: Classifique o tipo de um valor ===

def tipo_de(valor):
    if valor is None:
        return "nulo"
    if isinstance(valor, bool):
        return "booleano"
    if isinstance(valor, int):
        return "inteiro"
    if isinstance(valor, float):
        return "decimal"
    if isinstance(valor, str):
        return "texto"
    return "outro"


assert tipo_de(True) == "booleano"
assert tipo_de(7) == "inteiro"
assert tipo_de(2.5) == "decimal"
assert tipo_de("a") == "texto"
assert tipo_de(None) == "nulo"
assert tipo_de([1]) == "outro"
print("ok")
