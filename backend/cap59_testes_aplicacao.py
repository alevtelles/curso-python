"""Capítulo 59: Testes de aplicações.

Parte: Backend.
Execute com: python cap59_testes_aplicacao.py
"""


# === O que isolar: as fronteiras ===

from dataclasses import dataclass
from typing import Annotated, Protocol
from unittest.mock import Mock

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class PagamentoRecusado(Exception):
    pass


class GatewayPagamento(Protocol):
    def cobrar(self, valor_centavos: int) -> str: ...


class RepositorioPedidos(Protocol):
    def salvar(self, cliente: str, total_centavos: int, transacao: str) -> int: ...


class ServicoCheckout:
    def __init__(self, gateway: GatewayPagamento, repositorio: RepositorioPedidos) -> None:
        self._gateway = gateway
        self._repositorio = repositorio

    def finalizar(self, cliente: str, precos: list[int]) -> int:
        if not precos:
            raise ValueError("carrinho vazio")
        total = sum(precos)
        transacao = self._gateway.cobrar(total)
        return self._repositorio.salvar(cliente, total, transacao)


# === Fakes: implementações simples e honestas ===

class GatewayFalso:
    def __init__(self, recusar: bool = False) -> None:
        self.recusar = recusar
        self.cobrancas: list[int] = []

    def cobrar(self, valor_centavos: int) -> str:
        if self.recusar:
            raise PagamentoRecusado("cartão recusado")
        self.cobrancas.append(valor_centavos)
        return f"tx-{len(self.cobrancas)}"


class RepositorioEmMemoria:
    def __init__(self) -> None:
        self.pedidos: list[tuple[str, int, str]] = []

    def salvar(self, cliente: str, total_centavos: int, transacao: str) -> int:
        self.pedidos.append((cliente, total_centavos, transacao))
        return len(self.pedidos)


# === Testes unitários ===

def test_finaliza_cobrando_e_salvando():
    gateway, repositorio = GatewayFalso(), RepositorioEmMemoria()
    pedido_id = ServicoCheckout(gateway, repositorio).finalizar("Ana", [1000, 550])
    assert pedido_id == 1
    assert gateway.cobrancas == [1550]
    assert repositorio.pedidos == [("Ana", 1550, "tx-1")]


def test_pagamento_recusado_nao_grava_pedido():
    repositorio = RepositorioEmMemoria()
    with pytest.raises(PagamentoRecusado):
        ServicoCheckout(GatewayFalso(recusar=True), repositorio).finalizar("Ana", [500])
    assert repositorio.pedidos == []


def test_carrinho_vazio_nao_cobra():
    gateway = GatewayFalso()
    with pytest.raises(ValueError, match="vazio"):
        ServicoCheckout(gateway, RepositorioEmMemoria()).finalizar("Ana", [])
    assert gateway.cobrancas == []


@pytest.mark.parametrize("precos, esperado", [([100], 100), ([100, 200, 300], 600)])
def test_total_cobrado(precos, esperado):
    gateway = GatewayFalso()
    ServicoCheckout(gateway, RepositorioEmMemoria()).finalizar("Ana", precos)
    assert gateway.cobrancas == [esperado]


# === Quando um Mock faz sentido ===

def test_com_mock_verifica_a_interacao():
    gateway = Mock()
    gateway.cobrar.return_value = "tx-9"
    repositorio = Mock()
    repositorio.salvar.return_value = 7
    assert ServicoCheckout(gateway, repositorio).finalizar("Bia", [500]) == 7
    gateway.cobrar.assert_called_once_with(500)
    repositorio.salvar.assert_called_once_with("Bia", 500, "tx-9")


# === Testar a rota HTTP ===

class PedidoEntrada(BaseModel):
    cliente: str
    precos: list[int]


def montar_app(servico: ServicoCheckout) -> FastAPI:
    app = FastAPI()

    def obter_servico() -> ServicoCheckout:
        return servico

    @app.post("/checkout")
    def checkout(
        entrada: PedidoEntrada, svc: Annotated[ServicoCheckout, Depends(obter_servico)]
    ) -> dict[str, int]:
        try:
            return {"pedido_id": svc.finalizar(entrada.cliente, entrada.precos)}
        except PagamentoRecusado as erro:
            raise HTTPException(status_code=402, detail=str(erro)) from erro
        except ValueError as erro:
            raise HTTPException(status_code=422, detail=str(erro)) from erro

    return app


def test_rota_feliz():
    cliente = TestClient(montar_app(ServicoCheckout(GatewayFalso(), RepositorioEmMemoria())))
    resposta = cliente.post("/checkout", json={"cliente": "Ana", "precos": [100, 200]})
    assert resposta.status_code == 200
    assert resposta.json() == {"pedido_id": 1}


def test_rota_pagamento_recusado_devolve_402():
    cliente = TestClient(montar_app(ServicoCheckout(GatewayFalso(recusar=True), RepositorioEmMemoria())))
    assert cliente.post("/checkout", json={"cliente": "Ana", "precos": [100]}).status_code == 402


def test_rota_carrinho_vazio_devolve_422():
    cliente = TestClient(montar_app(ServicoCheckout(GatewayFalso(), RepositorioEmMemoria())))
    assert cliente.post("/checkout", json={"cliente": "Ana", "precos": []}).status_code == 422


# === Integração com o banco ===

class Base(DeclarativeBase):
    pass


class PedidoLinha(Base):
    __tablename__ = "pedidos_checkout"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente: Mapped[str]
    total_centavos: Mapped[int]
    transacao: Mapped[str]


class RepositorioSql:
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def salvar(self, cliente: str, total_centavos: int, transacao: str) -> int:
        linha = PedidoLinha(cliente=cliente, total_centavos=total_centavos, transacao=transacao)
        self._sessao.add(linha)
        self._sessao.commit()
        return linha.id


@pytest.fixture
def sessao():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as sessao_aberta:
        yield sessao_aberta


def test_repositorio_sql_grava_de_verdade(sessao):
    servico = ServicoCheckout(GatewayFalso(), RepositorioSql(sessao))
    servico.finalizar("Ana", [100, 200])
    servico.finalizar("Bia", [50])
    assert sessao.scalar(select(func.sum(PedidoLinha.total_centavos))) == 350
    assert sessao.scalar(select(func.count(PedidoLinha.id))) == 2


# === Exercício: O gateway falha no meio ===

def test_gateway_recusa_e_repositorio_nao_e_chamado():
    gateway = Mock()
    gateway.cobrar.side_effect = PagamentoRecusado("sem saldo")
    repositorio = Mock()
    with pytest.raises(PagamentoRecusado, match="sem saldo"):
        ServicoCheckout(gateway, repositorio).finalizar("Ana", [100])
    repositorio.salvar.assert_not_called()
