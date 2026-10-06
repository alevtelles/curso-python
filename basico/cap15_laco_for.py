"""Capítulo 15: Laços com for.

Parte: Júnior.
Execute com: python cap15_laco_for.py
"""


# === for em qualquer iterável ===

for letra in "abc":
    print(letra)

for fruta in ["maçã", "pera"]:
    print(fruta)


# === range ===

print(list(range(5)))
print(list(range(1, 6)))
print(list(range(0, 10, 2)))
print(list(range(5, 0, -1)))


# === enumerate e zip ===

nomes = ["Ana", "Bia", "Caio"]
for posicao, nome in enumerate(nomes, start=1):
    print(posicao, nome)

notas = [9, 8, 7]
for nome, nota in zip(nomes, notas):
    print(f"{nome}: {nota}")


# === break, continue e else ===

for numero in range(1, 11):
    if numero == 3:
        continue
    if numero == 6:
        break
    print(numero)
else:
    print("terminou sem break")

numero = 17
for divisor in range(2, numero):
    if numero % divisor == 0:
        print(f"{numero} não é primo")
        break
else:
    print(f"{numero} é primo")


# === Laços aninhados e padrões ===

for linhas in range(1, 5):
    print("*" * linhas)

for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}", end="  ")
    print()


# === Exercício: Fatorial ===

def fatorial(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


assert fatorial(5) == 120
assert fatorial(0) == 1
print("ok")


# === Exercício: Losango de asteriscos ===

def diamante(n):
    linhas = []
    for i in range(n):
        linhas.append(" " * (n - i - 1) + "*" * (2 * i + 1))
    for i in range(n - 2, -1, -1):
        linhas.append(" " * (n - i - 1) + "*" * (2 * i + 1))
    return linhas


assert diamante(3) == ["  *", " ***", "*****", " ***", "  *"]
print("\n".join(diamante(4)))


# === Exercício: Primos até n ===

def primos_ate(n):
    primos = []
    for candidato in range(2, n + 1):
        for divisor in range(2, candidato):
            if candidato % divisor == 0:
                break
        else:
            primos.append(candidato)
    return primos


assert primos_ate(20) == [2, 3, 5, 7, 11, 13, 17, 19]
print("ok")
