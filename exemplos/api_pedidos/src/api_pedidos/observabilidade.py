import json
import logging
import sys
from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

id_requisicao: ContextVar[str] = ContextVar("id_requisicao", default="-")

REQUISICOES = Counter("api_requisicoes_total", "Total de requisições", ["metodo", "rota", "status"])
LATENCIA = Histogram("api_latencia_segundos", "Latência das requisições", ["rota"])

log = logging.getLogger("api")


class FormatoJson(logging.Formatter):
    CAMPOS_EXTRAS = ("metodo", "rota", "status", "duracao_ms")

    def format(self, record: logging.LogRecord) -> str:
        dados: dict[str, object] = {
            "nivel": record.levelname,
            "mensagem": record.getMessage(),
            "id_requisicao": id_requisicao.get(),
        }
        for campo in self.CAMPOS_EXTRAS:
            if hasattr(record, campo):
                dados[campo] = getattr(record, campo)
        return json.dumps(dados, ensure_ascii=False)


def configurar_logs(nivel: str = "INFO") -> None:
    manipulador = logging.StreamHandler(sys.stdout)
    manipulador.setFormatter(FormatoJson())
    log.handlers = [manipulador]
    log.setLevel(nivel)
    log.propagate = False


def instalar_observabilidade(app: FastAPI) -> None:
    @app.middleware("http")
    async def medir(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        identificador = request.headers.get("X-Request-ID") or uuid4().hex
        token = id_requisicao.set(identificador)
        inicio = perf_counter()
        status = 500
        try:
            resposta = await call_next(request)
            status = resposta.status_code
        finally:
            duracao = perf_counter() - inicio
            rota_encontrada = request.scope.get("route")
            rota = getattr(rota_encontrada, "path", "desconhecida")
            REQUISICOES.labels(request.method, rota, str(status)).inc()
            LATENCIA.labels(rota).observe(duracao)
            log.info(
                "requisição concluída",
                extra={
                    "metodo": request.method,
                    "rota": rota,
                    "status": status,
                    "duracao_ms": round(duracao * 1000, 2),
                },
            )
            id_requisicao.reset(token)
        resposta.headers["X-Request-ID"] = identificador
        return resposta

    @app.get("/metricas", include_in_schema=False)
    def metricas() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
