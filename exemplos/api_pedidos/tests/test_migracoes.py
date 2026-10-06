from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

from api_pedidos.config import obter_configuracao

RAIZ = Path(__file__).resolve().parent.parent


def test_migracoes_estao_sincronizadas_com_os_modelos(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("API_DATABASE_URL", f"sqlite:///{tmp_path / 'migracao.db'}")
    obter_configuracao.cache_clear()
    cfg = Config(str(RAIZ / "alembic.ini"))
    try:
        command.upgrade(cfg, "head")
        command.check(cfg)  # falha se os modelos mudaram sem uma migração correspondente
    finally:
        obter_configuracao.cache_clear()
