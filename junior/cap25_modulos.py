"""Capítulo 25: Módulos e importação.

Parte: Júnior.
Execute com: python cap25_modulos.py
"""


# === Formas de importar ===

import math
from math import sqrt, pi
import datetime as dt

print(math.sqrt(16), sqrt(25))
print(f"{pi:.4f}")
print(math.floor(2.7), math.ceil(2.1), math.gcd(12, 18))


# === A biblioteca padrão ===

import statistics
from datetime import date, timedelta

notas = [7, 8, 9, 10]
print(statistics.mean(notas), statistics.median(notas))
hoje = date(2026, 10, 6)
print(hoje.strftime("%d/%m/%Y"))
print(hoje + timedelta(days=30))
print((date(2026, 12, 25) - hoje).days)

import random

print(random.randint(1, 6) in range(1, 7))
print(random.choice(["a", "b", "c"]) in "abc")


# === O padrão if __name__ == "__main__" ===

def main():
    print(f"executando com __name__ = {__name__!r}")


if __name__ == "__main__":
    main()


# === Como o Python encontra módulos ===

import sys

print(type(sys.path).__name__, "math" in sys.modules)


# === Exercício: Dias entre duas datas ===

from datetime import date


def dias_entre(inicio, fim):
    return (date.fromisoformat(fim) - date.fromisoformat(inicio)).days


assert dias_entre("2026-01-01", "2026-10-06") == 278
assert dias_entre("2026-10-06", "2026-10-06") == 0
print("ok")
