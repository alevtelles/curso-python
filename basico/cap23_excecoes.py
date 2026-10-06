"""Capítulo 23: Exceções.

Parte: Júnior.
Execute com: python cap23_excecoes.py
"""


# === Exceções são objetos organizados em hierarquia ===

print([c.__name__ for c in ZeroDivisionError.__mro__])


# === try, except, else e finally ===

def converter(texto):
    try:
        valor = int(texto)
    except ValueError:
        print(f"'{texto}' não é um inteiro")
        return None
    else:
        print("conversão feita")
        return valor
    finally:
        print("fim da tentativa")


print(converter("42"))
print(converter("abc"))


# === Capture apenas o que você sabe tratar ===

def dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return float("inf")
    except TypeError as erro:
        raise ValueError("os dois valores devem ser números") from erro


print(dividir(1, 0))
try:
    dividir(1, "a")
except ValueError as erro:
    print(erro, "|", type(erro.__cause__).__name__)


# === Exceções próprias ===

class SaldoInsuficiente(Exception):
    def __init__(self, saldo, valor):
        super().__init__(f"saldo {saldo} insuficiente para sacar {valor}")
        self.saldo = saldo
        self.valor = valor


def sacar(saldo, valor):
    if valor > saldo:
        raise SaldoInsuficiente(saldo, valor)
    return saldo - valor


try:
    sacar(100, 150)
except SaldoInsuficiente as erro:
    print(erro, erro.valor - erro.saldo)


# === Pedir perdão ou pedir licença ===

config = {"porta": 8080}

if "host" in config:
    host = config["host"]
else:
    host = "localhost"

try:
    host = config["host"]
except KeyError:
    host = "localhost"

print(host)


# === Exercício: Divisão segura ===

def dividir_seguro(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


assert dividir_seguro(10, 4) == 2.5
assert dividir_seguro(1, 0) is None
print("ok")


# === Exercício: Validar uma idade ===

def ler_idade(texto):
    try:
        idade = int(texto)
    except ValueError as erro:
        raise ValueError(f"idade inválida: {texto!r}") from erro
    if idade < 0:
        raise ValueError("idade não pode ser negativa")
    return idade


assert ler_idade("30") == 30
for entrada in ("abc", "-1"):
    try:
        ler_idade(entrada)
    except ValueError:
        pass
    else:
        raise AssertionError(f"{entrada!r} deveria falhar")
print("ok")
