"""Capítulo 16: Laços com while.

Parte: Júnior.
Execute com: python cap16_laco_while.py
"""


# === while ===

contagem = 3
while contagem > 0:
    print(contagem)
    contagem -= 1
print("Fogo!")


# === while True com break ===

while True:
    texto = input("Digite um número positivo: ")
    if texto.isdigit() and int(texto) > 0:
        break
    print("Valor inválido, tente de novo.")
print(f"Você digitou {int(texto)}")


# === Dígitos de um número ===

numero = 1234
while numero > 0:
    numero, digito = divmod(numero, 10)
    print(digito)

original = 12345
invertido = 0
while original > 0:
    original, digito = divmod(original, 10)
    invertido = invertido * 10 + digito
print(invertido)


# === Um jogo de adivinhação ===

import random

print(random.randint(1, 100) in range(1, 101))

segredo = 63
tentativas = 0
while True:
    palpite = int(input("Seu palpite: "))
    tentativas += 1
    if palpite < segredo:
        print("Muito baixo")
    elif palpite > segredo:
        print("Muito alto")
    else:
        print(f"Acertou em {tentativas} tentativas")
        break


# === Exercício: Soma dos dígitos ===

def soma_digitos(n):
    total = 0
    while n > 0:
        n, digito = divmod(n, 10)
        total += digito
    return total


assert soma_digitos(1234) == 10
assert soma_digitos(0) == 0
print("ok")


# === Exercício: Conjectura de Collatz ===

def collatz(n):
    passos = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        passos += 1
    return passos


assert collatz(6) == 8
assert collatz(1) == 0
print("ok")
