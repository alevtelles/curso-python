"""Capítulo 32: Comprehensions.

Parte: Intermediário.
Execute com: python cap32_comprehensions.py
"""


# === Listas, conjuntos e dicionários ===

quadrados = [n ** 2 for n in range(6)]
pares = [n for n in range(10) if n % 2 == 0]
print(quadrados)
print(pares)

palavras = ["python", "go", "rust"]
tamanhos = {p: len(p) for p in palavras}
unicos = {len(p) for p in palavras}
print(tamanhos, sorted(unicos))

rotulos = ["par" if n % 2 == 0 else "ímpar" for n in range(4)]
print(rotulos)


# === Compreensões aninhadas ===

matriz = [[1, 2, 3], [4, 5, 6]]
achatada = [n for linha in matriz for n in linha]
transposta = [[linha[i] for linha in matriz] for i in range(3)]
print(achatada)
print(transposta)


# === Expressões geradoras ===

soma = sum(n ** 2 for n in range(1000))
print(soma)

nomes = ["Ana", "Bia", "Caio"]
print(any(len(n) > 3 for n in nomes), all(n[0].isupper() for n in nomes))


# === Exercício: Transpor uma matriz ===

def transpor(matriz):
    return [list(coluna) for coluna in zip(*matriz)]


assert transpor([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
print("ok")


# === Exercício: Inverter chaves e valores ===

def inverter(d):
    return {valor: chave for chave, valor in d.items()}


assert inverter({"a": 1, "b": 2}) == {1: "a", 2: "b"}
print("ok")
