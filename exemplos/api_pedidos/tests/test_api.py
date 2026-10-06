from fastapi.testclient import TestClient

CORPO = {
    "cliente": "Ana",
    "itens": [
        {"produto": "caneta", "quantidade": 2, "preco_centavos": 350},
        {"produto": "caderno", "quantidade": 1, "preco_centavos": 1890},
    ],
}


def test_criar_pedido(cliente: TestClient) -> None:
    resposta = cliente.post("/pedidos", json=CORPO)
    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["total_centavos"] == 2590
    assert dados["status"] == "aberto"
    assert len(dados["itens"]) == 2


def test_idempotencia_devolve_o_mesmo_pedido(cliente: TestClient) -> None:
    cabecalho = {"Idempotency-Key": "abc-123"}
    primeira = cliente.post("/pedidos", json=CORPO, headers=cabecalho)
    segunda = cliente.post("/pedidos", json=CORPO, headers=cabecalho)
    assert primeira.status_code == 201
    assert segunda.status_code == 200
    assert primeira.json()["id"] == segunda.json()["id"]
    assert len(cliente.get("/pedidos").json()["itens"]) == 1


def test_validacao_recusa_corpo_invalido(cliente: TestClient) -> None:
    resposta = cliente.post("/pedidos", json={"cliente": "", "itens": []})
    assert resposta.status_code == 422


def test_pedido_inexistente_devolve_problema(cliente: TestClient) -> None:
    resposta = cliente.get("/pedidos/999")
    assert resposta.status_code == 404
    assert resposta.headers["content-type"].startswith("application/problem+json")
    assert resposta.json()["titulo"] == "Pedido não encontrado"


def test_cancelar_duas_vezes_devolve_conflito(cliente: TestClient) -> None:
    pedido_id = cliente.post("/pedidos", json=CORPO).json()["id"]
    assert cliente.post(f"/pedidos/{pedido_id}/cancelar").json()["status"] == "cancelado"
    assert cliente.post(f"/pedidos/{pedido_id}/cancelar").status_code == 409


def test_paginacao_por_cursor(cliente: TestClient) -> None:
    for _ in range(5):
        cliente.post("/pedidos", json=CORPO)
    primeira = cliente.get("/pedidos", params={"limite": 2}).json()
    assert len(primeira["itens"]) == 2
    assert primeira["proximo_cursor"] == 2
    ultima = cliente.get("/pedidos", params={"limite": 2, "cursor": 4}).json()
    assert [p["id"] for p in ultima["itens"]] == [5]
    assert ultima["proximo_cursor"] is None


def test_saude_e_metricas(cliente: TestClient) -> None:
    assert cliente.get("/saude").json() == {"banco": "ok"}
    cliente.get("/pedidos")
    assert "api_requisicoes_total" in cliente.get("/metricas").text


def test_id_de_requisicao_e_devolvido(cliente: TestClient) -> None:
    resposta = cliente.get("/saude", headers={"X-Request-ID": "req-42"})
    assert resposta.headers["x-request-id"] == "req-42"
