"""Capítulo 21: Dicionários.

Parte: Júnior.
Execute com: python cap21_dicionarios.py
"""


# === Chaves e valores ===

pessoa = {"nome": "Ana", "idade": 30}
print(pessoa["nome"])
pessoa["cidade"] = "Recife"
pessoa["idade"] = 31
del pessoa["nome"]
print(pessoa)


# === Acessar com segurança ===

try:
    pessoa["email"]
except KeyError as erro:
    print("KeyError:", erro)
print(pessoa.get("email"))
print(pessoa.get("email", "sem email"))
print("idade" in pessoa)


# === Percorrer e alterar ===

estoque = {"maçã": 10, "pera": 0, "uva": 25}
for fruta, quantidade in estoque.items():
    print(f"{fruta}: {quantidade}")
print(list(estoque.keys()))
print(list(estoque.values()))
estoque.update({"pera": 5, "kiwi": 3})
print(estoque.pop("kiwi"))
print(estoque.setdefault("manga", 0))
print(estoque)

a = {"x": 1, "y": 2}
b = {"y": 20, "z": 30}
print(a | b)
print({**a, **b})


# === Contar e agrupar ===

from collections import Counter, defaultdict

palavras = ["a", "b", "a", "c", "b", "a"]

contagem = {}
for palavra in palavras:
    contagem[palavra] = contagem.get(palavra, 0) + 1
print(contagem)

print(Counter(palavras))
print(Counter(palavras).most_common(1))

por_inicial = defaultdict(list)
for nome in ["Ana", "Alice", "Bia", "Caio", "Beto"]:
    por_inicial[nome[0]].append(nome)
print(dict(por_inicial))


# === Dados aninhados ===

pedido = {
    "cliente": "Ana",
    "itens": [
        {"produto": "caneta", "qtd": 2},
        {"produto": "caderno", "qtd": 1},
    ],
}
total_itens = 0
for item in pedido["itens"]:
    total_itens += item["qtd"]
print(total_itens)


# === Exercício: Frequência de cada elemento ===

def frequencia(itens):
    resultado = {}
    for item in itens:
        resultado[item] = resultado.get(item, 0) + 1
    return resultado


assert frequencia(["a", "b", "a", "c", "b", "a"]) == {"a": 3, "b": 2, "c": 1}
print("ok")


# === Exercício: Somar dicionários ===

def somar_dicts(d1, d2):
    resultado = dict(d1)
    for chave, valor in d2.items():
        resultado[chave] = resultado.get(chave, 0) + valor
    return resultado


assert somar_dicts({"a": 5, "b": 3}, {"b": 4, "c": 2}) == {"a": 5, "b": 7, "c": 2}
print("ok")
