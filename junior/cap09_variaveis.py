"""Capítulo 9: Comentários e variáveis.

Parte: Júnior.
Execute com: python cap09_variaveis.py
"""


# === Comentários ===

# Comentário de uma linha
idade = 30  # comentário no fim da linha

"""
Isto é uma string de várias linhas.
O Python a avalia e descarta, mas ela não é um comentário de verdade.
"""
print(idade)

def area_quadrado(lado):
    """Devolve a área de um quadrado de lado dado."""
    return lado * lado


print(area_quadrado.__doc__)


# === Variáveis são nomes ===

nome = "Ana"
idade = 30
cidade = "Recife"
print(nome, idade, cidade)

valor = 10
print(type(valor))
valor = "dez"
print(type(valor))

a, b = 1, 2
a, b = b, a
print(a, b)

x = y = 0
print(x, y)


# === Nomes válidos e convenções ===

import keyword

print(keyword.iskeyword("class"))
print(keyword.iskeyword("nome"))
print(len(keyword.kwlist) > 30)


# === Exercício: Troque dois valores sem criar uma terceira variável ===

a, b = 3, 7
a, b = b, a
assert (a, b) == (7, 3)
print("ok")
