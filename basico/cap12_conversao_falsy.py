"""Capítulo 12: Conversão de tipos e valores falsy.

Parte: Júnior.
Execute com: python cap12_conversao_falsy.py
"""


# === Conversão explícita ===

print(int("42") + 1)
print(float("3.5") * 2)
print(str(10) + " anos")
print(int(3.9), int(-3.9))
print(round(3.5), round(4.5), round(3.14159, 2))

try:
    int("abc")
except ValueError as erro:
    print(erro)


# === Conversão implícita ===

print(1 + 2.5)
print(True + 1)
print(type(6 / 2), type(6 // 2))


# === Valores falsy ===

valores = [None, False, 0, 0.0, "", [], (), {}, set(), range(0)]
print([bool(v) for v in valores])

print(bool("0"), bool("False"), bool([0]), bool(" "))


# === Falsy não é o mesmo que None ===

def descricao(quantidade):
    if quantidade is None:
        return "não informado"
    if not quantidade:
        return "zero"
    return f"{quantidade} unidades"


print(descricao(None))
print(descricao(0))
print(descricao(5))


# === Exercício: Números no formato brasileiro ===

def para_float(texto):
    return float(texto.replace(".", "").replace(",", "."))


assert para_float("12,5") == 12.5
assert para_float("1.234,56") == 1234.56
print("ok")
