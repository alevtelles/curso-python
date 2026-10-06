"""Funções de apoio importadas pelo programa principal."""


def saudacao(nome: str) -> str:
    return f"Olá, {nome}!"


if __name__ == "__main__":
    print(saudacao("teste do módulo"))
