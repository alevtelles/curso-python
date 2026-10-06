import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from api_pedidos.esquemas import ItemCriar, PedidoCriar
from api_pedidos.modelos import Pedido
from api_pedidos.repositorio import RepositorioPedidos
from api_pedidos.servico import PedidoNaoEncontrado, ServicoPedidos

DADOS = PedidoCriar(
    cliente="Ana", itens=[ItemCriar(produto="caneta", quantidade=1, preco_centavos=100)]
)


def test_obter_pedido_inexistente(engine: Engine) -> None:
    with Session(engine) as sessao, pytest.raises(PedidoNaoEncontrado):
        ServicoPedidos(sessao).obter(1)


def test_corrida_de_chaves_devolve_o_pedido_existente(
    engine: Engine, monkeypatch: pytest.MonkeyPatch
) -> None:
    with Session(engine) as sessao:
        original, criado = ServicoPedidos(sessao).criar(DADOS, "chave-1")
        assert criado
        original_id = original.id

    chamadas = {"total": 0}
    por_chave_real = RepositorioPedidos.por_chave

    def por_chave_atrasada(self: RepositorioPedidos, chave: str) -> Pedido | None:
        chamadas["total"] += 1
        if chamadas["total"] == 1:
            return None  # simula a outra requisição ainda não ter gravado
        return por_chave_real(self, chave)

    monkeypatch.setattr(RepositorioPedidos, "por_chave", por_chave_atrasada)
    with Session(engine) as sessao:
        pedido, criado = ServicoPedidos(sessao).criar(DADOS, "chave-1")
        assert criado is False
        assert pedido.id == original_id
