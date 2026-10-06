"""Capítulo 51: Arquitetura e erros em produção.

Parte: Avançado.
Execute com: python cap51_arquitetura.py
"""


# === Separar a regra de negócio do mundo externo ===

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Pedido:
    id: str
    cliente: str
    total: float


class RepositorioPedidos(Protocol):
    def salvar(self, pedido: Pedido) -> None: ...
    def existe(self, pedido_id: str) -> bool: ...


class Notificador(Protocol):
    def enviar(self, destinatario: str, mensagem: str) -> None: ...


class PedidoDuplicado(Exception):
    pass


class ServicoPedidos:
    def __init__(self, repositorio: RepositorioPedidos, notificador: Notificador) -> None:
        self._repositorio = repositorio
        self._notificador = notificador

    def registrar(self, pedido: Pedido) -> None:
        if self._repositorio.existe(pedido.id):
            raise PedidoDuplicado(pedido.id)
        self._repositorio.salvar(pedido)
        self._notificador.enviar(pedido.cliente, f"pedido {pedido.id} recebido")

class RepositorioEmMemoria:
    def __init__(self) -> None:
        self._dados: dict[str, Pedido] = {}

    def salvar(self, pedido: Pedido) -> None:
        self._dados[pedido.id] = pedido

    def existe(self, pedido_id: str) -> bool:
        return pedido_id in self._dados


class NotificadorFalso:
    def __init__(self) -> None:
        self.enviadas: list[tuple[str, str]] = []

    def enviar(self, destinatario: str, mensagem: str) -> None:
        self.enviadas.append((destinatario, mensagem))


notificador = NotificadorFalso()
servico = ServicoPedidos(RepositorioEmMemoria(), notificador)
servico.registrar(Pedido("p1", "ana", 50.0))
print(notificador.enviadas)
try:
    servico.registrar(Pedido("p1", "ana", 50.0))
except PedidoDuplicado as erro:
    print("duplicado:", erro)


# === Configuração fora do código ===

import os
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Configuracao:
    ambiente: str
    timeout_segundos: float
    url_banco: str

    @classmethod
    def do_ambiente(cls, env: Mapping[str, str] | None = None) -> "Configuracao":
        env = os.environ if env is None else env
        return cls(
            ambiente=env.get("APP_AMBIENTE", "desenvolvimento"),
            timeout_segundos=float(env.get("APP_TIMEOUT", "5")),
            url_banco=env["APP_URL_BANCO"],
        )


config = Configuracao.do_ambiente(
    {"APP_URL_BANCO": "postgresql://localhost/app", "APP_TIMEOUT": "2.5"}
)
print(config)
try:
    Configuracao.do_ambiente({})
except KeyError as erro:
    print("variável obrigatória ausente:", erro)


# === Retentativas com espera crescente ===

import random
import time
from collections.abc import Callable


def com_retentativas[T](
    operacao: Callable[[], T],
    *,
    tentativas: int = 4,
    base: float = 0.5,
    dormir: Callable[[float], None] = time.sleep,
    jitter: Callable[[], float] = random.random,
) -> T:
    for numero in range(1, tentativas + 1):
        try:
            return operacao()
        except ConnectionError:
            if numero == tentativas:
                raise
            espera = base * 2 ** (numero - 1) * (0.5 + jitter() / 2)
            dormir(espera)
    raise AssertionError("inalcançável")


esperas: list[float] = []
chamadas = {"total": 0}


def instavel() -> str:
    chamadas["total"] += 1
    if chamadas["total"] < 3:
        raise ConnectionError("falha")
    return "ok"


resultado = com_retentativas(instavel, dormir=esperas.append, jitter=lambda: 1.0)
print(resultado, esperas)


# === Logs que se conectam ===

import contextvars
import json
import logging
import sys

id_requisicao = contextvars.ContextVar("id_requisicao", default="-")


class FiltroDeContexto(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        setattr(record, "id_requisicao", id_requisicao.get())
        return True


class FormatoJson(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "nivel": record.levelname,
                "mensagem": record.getMessage(),
                "id_requisicao": getattr(record, "id_requisicao", "-"),
            },
            ensure_ascii=False,
        )


manipulador = logging.StreamHandler(sys.stdout)
manipulador.setFormatter(FormatoJson())
manipulador.addFilter(FiltroDeContexto())
log = logging.getLogger("api")
log.addHandler(manipulador)
log.setLevel(logging.INFO)
log.propagate = False


def tratar(id_: str) -> None:
    token = id_requisicao.set(id_)
    try:
        log.info("pedido processado")
    finally:
        id_requisicao.reset(token)


tratar("req-1")
tratar("req-2")
log.info("fora de requisição")


# === Erros: traduza na fronteira ===

def para_resposta(excecao: Exception) -> tuple[int, str]:
    if isinstance(excecao, PedidoDuplicado):
        return 409, "pedido já registrado"
    if isinstance(excecao, ValueError):
        return 422, str(excecao)
    return 500, "erro interno"


print(para_resposta(PedidoDuplicado("p1")), para_resposta(RuntimeError("segredo")))


# === Exercício: Teste a regra de duplicidade ===

def testar_duplicidade():
    notificador = NotificadorFalso()
    servico = ServicoPedidos(RepositorioEmMemoria(), notificador)
    servico.registrar(Pedido("a", "bia", 10.0))
    try:
        servico.registrar(Pedido("a", "bia", 10.0))
    except PedidoDuplicado:
        pass
    else:
        raise AssertionError("deveria levantar PedidoDuplicado")
    assert len(notificador.enviadas) == 1


testar_duplicidade()
print("ok")
