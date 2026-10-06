import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import StaticPool

from api_pedidos.app import criar_app
from api_pedidos.modelos import Base


@pytest.fixture
def engine() -> Iterator[Engine]:
    """SQLite em memória por padrão. Defina TEST_DATABASE_URL para testar contra PostgreSQL."""
    url = os.environ.get("TEST_DATABASE_URL")
    if url:
        eng = create_engine(url)
    else:
        eng = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()


@pytest.fixture
def cliente(engine: Engine) -> TestClient:
    return TestClient(criar_app(engine))
