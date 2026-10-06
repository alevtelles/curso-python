"""Capítulo 11: Strings.

Parte: Júnior.
Execute com: python cap11_strings.py
"""


# === Índices e fatias ===

texto = "Python"
print(texto[0], texto[-1], texto[1:4], texto[::-1])


# === Strings não mudam ===

try:
    texto[0] = "J"
except TypeError as erro:
    print(erro)

novo = "J" + texto[1:]
print(novo)


# === Os métodos do dia a dia ===

frase = "  Aprender Python é divertido  "
print(frase.strip())
print(frase.strip().lower())
print(frase.strip().upper())
print(frase.strip().split())
print("-".join(["a", "b", "c"]))
print(frase.replace("Python", "Go").strip())
print(frase.find("Python"))
print(frase.strip().startswith("Aprender"))
print(frase.count("e"))
print("Python" in frase)


# === f-strings ===

nome = "Ana"
preco = 1234.5
quantidade = 3
print(f"{nome} comprou {quantidade} itens")
print(f"Preço: {preco:,.2f}")
print(f"Total: {preco * quantidade:.2f}")
print(f"[{nome:>8}] [{nome:<8}] [{nome:^8}]")
print(f"{quantidade=}")

preco = 1234.5
americano = f"{preco:,.2f}"
brasileiro = americano.replace(",", "_").replace(".", ",").replace("_", ".")
print(brasileiro)


# === Unicode e bytes ===

print(ord("A"), chr(97))
palavra = "ação"
print(len(palavra))
dados = palavra.encode("utf-8")
print(dados)
print(len(dados))
print(dados.decode("utf-8"))


# === Exercício: Palíndromo ===

def eh_palindromo(texto):
    limpo = texto.lower().replace(" ", "")
    return limpo == limpo[::-1]


assert eh_palindromo("Anotaram a data da maratona")
assert eh_palindromo("radar")
assert not eh_palindromo("python")
print("ok")


# === Exercício: Inverter a ordem das palavras ===

def inverter_palavras(frase):
    return " ".join(frase.split()[::-1])


assert inverter_palavras("python é bom") == "bom é python"
print("ok")
