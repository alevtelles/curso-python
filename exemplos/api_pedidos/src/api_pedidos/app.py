from typing import Annotated

from fastapi import Depends, FastAPI, Header, Query, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session

from api_pedidos.config import obter_configuracao
from api_pedidos.db import criar_engine, criar_fabrica_de_sessoes, obter_sessao
from api_pedidos.esquemas import Pagina, PedidoCriar, PedidoLer
from api_pedidos.observabilidade import configurar_logs, instalar_observabilidade
from api_pedidos.servico import PedidoJaCancelado, PedidoNaoEncontrado, ServicoPedidos

SessaoDep = Annotated[Session, Depends(obter_sessao)]


def obter_servico(sessao: SessaoDep) -> ServicoPedidos:
    return ServicoPedidos(sessao)


ServicoDep = Annotated[ServicoPedidos, Depends(obter_servico)]


def problema(status: int, titulo: str, detalhe: str) -> JSONResponse:
    """Formato de erro único para toda a API (inspirado no RFC 9457)."""
    return JSONResponse(
        {"titulo": titulo, "status": status, "detalhe": detalhe},
        status_code=status,
        media_type="application/problem+json",
    )


def criar_app(engine: Engine | None = None) -> FastAPI:
    config = obter_configuracao()
    configurar_logs(config.log_nivel)
    engine = engine or criar_engine(config.database_url.get_secret_value())
    app = FastAPI(title="API de pedidos", version="0.1.0")
    app.state.engine = engine
    app.state.fabrica = criar_fabrica_de_sessoes(engine)
    instalar_observabilidade(app)

    @app.exception_handler(PedidoNaoEncontrado)
    def nao_encontrado(_: Request, erro: PedidoNaoEncontrado) -> JSONResponse:
        return problema(404, "Pedido não encontrado", str(erro))

    @app.exception_handler(PedidoJaCancelado)
    def ja_cancelado(_: Request, erro: PedidoJaCancelado) -> JSONResponse:
        return problema(409, "Conflito de estado", str(erro))

    @app.post("/pedidos", response_model=PedidoLer, status_code=201)
    def criar_pedido(
        dados: PedidoCriar,
        servico: ServicoDep,
        resposta: Response,
        idempotency_key: Annotated[str | None, Header(max_length=80)] = None,
    ) -> object:
        pedido, criado = servico.criar(dados, idempotency_key)
        if not criado:
            resposta.status_code = 200
        return pedido

    @app.get("/pedidos/{pedido_id}", response_model=PedidoLer)
    def obter_pedido(pedido_id: int, servico: ServicoDep) -> object:
        return servico.obter(pedido_id)

    @app.get("/pedidos", response_model=Pagina)
    def listar_pedidos(
        servico: ServicoDep,
        limite: Annotated[int, Query(ge=1, le=100)] = 20,
        cursor: Annotated[int, Query(ge=0)] = 0,
    ) -> object:
        pagina, proximo = servico.listar(cursor, limite)
        return {"itens": pagina, "proximo_cursor": proximo}

    @app.post("/pedidos/{pedido_id}/cancelar", response_model=PedidoLer)
    def cancelar_pedido(pedido_id: int, servico: ServicoDep) -> object:
        return servico.cancelar(pedido_id)

    @app.get("/saude")
    def saude(sessao: SessaoDep) -> JSONResponse:
        try:
            sessao.execute(text("SELECT 1"))
        except Exception:
            return JSONResponse({"banco": "indisponível"}, status_code=503)
        return JSONResponse({"banco": "ok"})

    return app
