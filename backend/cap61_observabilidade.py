"""Capítulo 61: Observabilidade.

Parte: Backend.
Execute com: python cap61_observabilidade.py
"""


# === Logs estruturados com identificador de correlação ===

import contextvars
import json
import logging
import sys
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

id_requisicao = contextvars.ContextVar("id_requisicao", default="-")


class FormatoJson(logging.Formatter):
    def format(self, record):
        return json.dumps(
            {
                "nivel": record.levelname,
                "mensagem": record.getMessage(),
                "id_requisicao": id_requisicao.get(),
            },
            ensure_ascii=False,
        )


manipulador = logging.StreamHandler(sys.stdout)
manipulador.setFormatter(FormatoJson())
log = logging.getLogger("loja")
log.handlers = [manipulador]
log.setLevel(logging.INFO)
log.propagate = False

app = FastAPI()


@app.middleware("http")
async def correlacionar(request: Request, call_next):
    identificador = request.headers.get("X-Request-ID") or uuid4().hex[:8]
    token = id_requisicao.set(identificador)
    try:
        resposta = await call_next(request)
    finally:
        id_requisicao.reset(token)
    resposta.headers["X-Request-ID"] = identificador
    return resposta


@app.get("/pedido/{numero}")
def pedido(numero: int):
    log.info("buscando pedido %d", numero)
    return {"numero": numero}


cliente = TestClient(app)
resposta = cliente.get("/pedido/7", headers={"X-Request-ID": "abc123"})
print(resposta.headers["x-request-id"])


# === Métricas com Prometheus ===

from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest

registro = CollectorRegistry()
PEDIDOS = Counter("pedidos_total", "Pedidos criados", ["status"], registry=registro)
LATENCIA = Histogram("checkout_segundos", "Duração do checkout", buckets=(0.1, 0.5, 1.0), registry=registro)

PEDIDOS.labels("aprovado").inc()
PEDIDOS.labels("aprovado").inc()
PEDIDOS.labels("recusado").inc()
LATENCIA.observe(0.3)
LATENCIA.observe(0.05)

texto = generate_latest(registro).decode()
interessantes = ("pedidos_total{", "checkout_segundos_bucket", "checkout_segundos_count")
print("\n".join(linha for linha in texto.splitlines() if linha.startswith(interessantes)))


# === Traces com OpenTelemetry ===

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

exportador = InMemorySpanExporter()
provedor = TracerProvider()
provedor.add_span_processor(SimpleSpanProcessor(exportador))
rastreador = provedor.get_tracer("loja")

with rastreador.start_as_current_span("checkout") as raiz:
    raiz.set_attribute("cliente", "Ana")
    with rastreador.start_as_current_span("cobrar_cartao"):
        pass
    with rastreador.start_as_current_span("gravar_pedido") as etapa:
        etapa.set_attribute("itens", 3)

spans = exportador.get_finished_spans()
nomes = {s.context.span_id: s.name for s in spans}
for s in spans:
    pai = nomes.get(s.parent.span_id) if s.parent else None
    print(f"{s.name:<14} pai={pai} atributos={dict(s.attributes)}")


# === Exercício: Contar requisições por rota ===

registro_exercicio = CollectorRegistry()
REQUISICOES = Counter("req", "Requisições", ["rota"], registry=registro_exercicio)

app_exercicio = FastAPI()


@app_exercicio.middleware("http")
async def contar(request: Request, call_next):
    resposta = await call_next(request)
    rota = getattr(request.scope.get("route"), "path", "desconhecida")
    REQUISICOES.labels(rota).inc()
    return resposta


@app_exercicio.get("/ping")
def ping():
    return {"ok": True}


cliente_exercicio = TestClient(app_exercicio)
cliente_exercicio.get("/ping")
cliente_exercicio.get("/ping")
assert registro_exercicio.get_sample_value("req_total", {"rota": "/ping"}) == 2.0
print("ok")
