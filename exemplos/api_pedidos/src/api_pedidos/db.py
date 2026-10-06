from collections.abc import Iterator
from typing import Any

from fastapi import Request
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def criar_engine(url: str) -> Engine:
    argumentos: dict[str, Any] = {}
    if url.startswith("sqlite"):
        argumentos["check_same_thread"] = False
    return create_engine(url, connect_args=argumentos, pool_pre_ping=True)


def criar_fabrica_de_sessoes(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)


def obter_sessao(request: Request) -> Iterator[Session]:
    with request.app.state.fabrica() as sessao:
        yield sessao
