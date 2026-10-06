"""Capítulo 17: Funções.

Parte: Júnior.
Execute com: python cap17_funcoes.py
"""


# === Definir, chamar e devolver ===

def saudacao(nome):
    """Devolve uma saudação."""
    return f"Olá, {nome}!"


def sem_retorno():
    pass


print(saudacao("Ana"))
print(sem_retorno())


# === Parâmetros e argumentos ===

def criar_usuario(nome, /, email, *, ativo=True):
    return {"nome": nome, "email": email, "ativo": ativo}


print(criar_usuario("Ana", "ana@exemplo.com"))
print(criar_usuario("Bia", email="bia@exemplo.com", ativo=False))
try:
    criar_usuario(nome="Caio", email="c@exemplo.com")
except TypeError as erro:
    print(erro)


# === *args e **kwargs ===

def somar(*numeros):
    return sum(numeros)


def descrever(**atributos):
    for chave, valor in atributos.items():
        print(f"{chave}: {valor}")


print(somar(1, 2, 3, 4))
descrever(nome="Ana", cidade="Recife")

valores = [10, 20, 30]
print(somar(*valores))
dados = {"nome": "Bia", "cidade": "Natal"}
descrever(**dados)


# === Vários valores de retorno ===

def minimo_maximo(numeros):
    return min(numeros), max(numeros)


menor, maior = minimo_maximo([4, 8, 2, 9])
print(menor, maior)


# === Funções são objetos ===

def aplicar(funcao, valor):
    return funcao(valor)


print(aplicar(len, "python"))
print(aplicar(str.upper, "python"))


# === Documentação e type hints ===

def soma(a: int, b: int) -> int:
    """Soma dois inteiros e devolve o resultado."""
    return a + b


print(soma(2, 3))
print(soma("a", "b"))


# === Exercício: Média de quantos números quiser ===

def media(*numeros):
    return sum(numeros) / len(numeros)


assert media(10, 20, 30) == 20
assert media(5) == 5
print("ok")


# === Exercício: Nome completo com opção ===

def formatar_nome(nome, sobrenome, *, maiusculo=False):
    completo = f"{nome} {sobrenome}"
    return completo.upper() if maiusculo else completo


assert formatar_nome("Ana", "Lima") == "Ana Lima"
assert formatar_nome("Ana", "Lima", maiusculo=True) == "ANA LIMA"
print("ok")
