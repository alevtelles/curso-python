"""Capítulo 14: Condicionais.

Parte: Júnior.
Execute com: python cap14_condicionais.py
"""


# === if, elif e else ===

def classificar(nota):
    if nota >= 9:
        return "excelente"
    elif nota >= 7:
        return "bom"
    elif nota >= 5:
        return "regular"
    else:
        return "insuficiente"


print(classificar(9.5))
print(classificar(7))
print(classificar(5))
print(classificar(2))


# === Expressão condicional ===

idade = 20
situacao = "adulto" if idade >= 18 else "menor"
print(situacao)


# === match: casamento de padrões ===

def responder(comando):
    match comando.split():
        case ["parar"]:
            return "parando"
        case ["mover", direcao]:
            return f"movendo para {direcao}"
        case ["mover", direcao, passos] if passos.isdigit():
            return f"movendo {passos} passos para {direcao}"
        case _:
            return "comando desconhecido"


print(responder("parar"))
print(responder("mover norte"))
print(responder("mover sul 3"))
print(responder("voar"))


# === Idiomas que deixam o código limpo ===

def desconto(preco, cliente_vip):
    if preco <= 0:
        return 0
    if not cliente_vip:
        return 0
    return preco * 0.1


print(desconto(200, True))


# === Exercício: Ano bissexto ===

def eh_bissexto(ano):
    return ano % 400 == 0 or (ano % 4 == 0 and ano % 100 != 0)


assert eh_bissexto(2024)
assert eh_bissexto(2000)
assert not eh_bissexto(1900)
assert not eh_bissexto(2023)
print("ok")


# === Exercício: Escada de temperatura ===

def descrever(temperatura):
    if temperatura < 10:
        return "frio"
    elif temperatura < 28:
        return "agradável"
    return "quente"


assert descrever(-5) == "frio"
assert descrever(25) == "agradável"
assert descrever(45) == "quente"
print("ok")
