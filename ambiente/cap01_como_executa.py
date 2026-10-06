"""Capítulo 1: O que é Python e como ele executa.

Parte: Ambiente.
Execute com: python cap01_como_executa.py
"""


# === Python em poucas palavras ===

print("Olá, Python")


# === Compilado ou interpretado: os dois ===

codigo = "print('primeira linha')\nprint('segunda linha'"

try:
    compile(codigo, "<exemplo>", "exec")
except SyntaxError as erro:
    print("Nada foi executado. Erro de sintaxe:", erro.msg)

def dividir(a, b):
    return a / b

print("esta linha roda normalmente")
try:
    dividir(1, 0)
except ZeroDivisionError as erro:
    print("erro só apareceu na execução:", erro)

import dis


def soma(a, b):
    return a + b


dis.dis(soma)
