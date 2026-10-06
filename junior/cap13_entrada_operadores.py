"""Capítulo 13: Entrada, saída e operadores.

Parte: Júnior.
Execute com: python cap13_entrada_operadores.py
"""


# === print ===

print("a", "b", "c", sep="-")
print("sem quebra", end=" ")
print("de linha")


# === input ===

nome = input("Qual é o seu nome? ")
idade = int(input("Quantos anos você tem? "))
print(f"Olá, {nome}. Em 5 anos você terá {idade + 5} anos.")


# === Operadores aritméticos ===

print(10 / 3)
print(10 // 3)
print(-7 // 2)
print(10 % 3)
print(2 ** 8)
print(divmod(17, 5))


# === Comparação e operadores lógicos ===

x = 7
print(1 < x < 10)
print(x == 7.0)
print("a" < "b")

nome = "" or "anônimo"
print(nome)
print(0 and 5)
print(3 and 5)
print(not [])


# === Pertencimento e identidade ===

print("py" in "python", 3 not in [1, 2])
valor = None
print(valor is None, valor is not None)


# === Atribuição composta e o operador morsa ===

total = 10
total += 5
total *= 2
total //= 4
print(total)

if (n := len("python")) > 5:
    print(f"{n} caracteres")


# === Exercício: Converter segundos em horas, minutos e segundos ===

def decompor(segundos):
    horas, resto = divmod(segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    return horas, minutos, segundos


assert decompor(3725) == (1, 2, 5)
assert decompor(59) == (0, 0, 59)
print("ok")
