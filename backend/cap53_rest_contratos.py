"""Capítulo 53: REST e fundamentos de APIs.

Parte: Backend.
Execute com: python cap53_rest_contratos.py
"""


# === Paginação: por deslocamento ou por cursor ===

itens = list(range(1, 11))


def por_deslocamento(itens, deslocamento, limite):
    return itens[deslocamento : deslocamento + limite]


pagina_1 = por_deslocamento(itens, 0, 3)
itens.insert(0, 0)  # alguém cria um item no começo enquanto você navega
pagina_2 = por_deslocamento(itens, 3, 3)
print(pagina_1, pagina_2)

itens = list(range(1, 11))


def por_cursor(itens, depois_de, limite):
    pagina = [i for i in itens if i > depois_de][:limite]
    proximo = pagina[-1] if len(pagina) == limite else None
    return pagina, proximo


pagina_1, cursor = por_cursor(itens, 0, 3)
itens.insert(0, 0)
pagina_2, cursor = por_cursor(itens, cursor, 3)
print(pagina_1, pagina_2)


# === Erros com um formato único ===

def problema(status, tipo, titulo, detalhe, **extras):
    return {
        "tipo": f"https://exemplo.com/erros/{tipo}",
        "titulo": titulo,
        "status": status,
        "detalhe": detalhe,
        **extras,
    }


print(problema(409, "pedido-ja-cancelado", "Conflito de estado", "O pedido 7 já está cancelado.", pedido_id=7))


# === Idempotência no POST ===

resultados = {}


def criar_pedido(chave, dados):
    if chave in resultados:
        return 200, resultados[chave]
    pedido = {"id": len(resultados) + 1, **dados}
    resultados[chave] = pedido
    return 201, pedido


print(criar_pedido("k1", {"cliente": "Ana"}))
print(criar_pedido("k1", {"cliente": "Ana"}))
print(criar_pedido("k2", {"cliente": "Bia"}))


# === Exercício: Paginação por cursor ===

def paginar(itens, cursor, limite):
    pagina = [i for i in itens if i > cursor][: limite + 1]
    proximo = pagina[limite - 1] if len(pagina) > limite else None
    return {"itens": pagina[:limite], "proximo_cursor": proximo}


assert paginar(list(range(1, 8)), 0, 3) == {"itens": [1, 2, 3], "proximo_cursor": 3}
assert paginar(list(range(1, 8)), 6, 3) == {"itens": [7], "proximo_cursor": None}
print("ok")
