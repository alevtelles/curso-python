"""Capítulo 50: Qualidade e automação.

Parte: Avançado.
Execute com: python cap50_qualidade.py
"""


# === Lint e formatação com ruff ===

def adicionar(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista


assert adicionar(1) == [1]
assert adicionar(2) == [2]
print("sem os problemas apontados")


# === Exercício: Teste de regressão ===

def teste_adicionar_nao_compartilha_estado():
    assert adicionar(1) == [1]
    assert adicionar(2) == [2]


teste_adicionar_nao_compartilha_estado()
print("ok")
