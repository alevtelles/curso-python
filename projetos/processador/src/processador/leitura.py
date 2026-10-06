import asyncio
import logging
from collections.abc import Awaitable, Callable
from pathlib import Path

log = logging.getLogger(__name__)


def ler_texto(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8")


async def ler_com_retentativas(
    caminho: Path,
    *,
    tentativas: int = 3,
    base: float = 0.1,
    dormir: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ler: Callable[[Path], str] = ler_texto,
) -> str:
    """Lê o arquivo em uma thread, para não bloquear o laço de eventos, com espera crescente."""
    for numero in range(1, tentativas + 1):
        try:
            return await asyncio.to_thread(ler, caminho)
        except OSError as erro:
            if numero == tentativas:
                raise
            espera = base * 2 ** (numero - 1)
            log.warning(
                "leitura falhou (%s), tentativa %d, nova tentativa em %.2fs", erro, numero, espera
            )
            await dormir(espera)
    raise AssertionError("inalcançável")
