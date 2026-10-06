import asyncio
import logging
import multiprocessing
from collections.abc import Awaitable, Callable
from concurrent.futures import Executor, ProcessPoolExecutor
from pathlib import Path

from processador.calculo import agregar
from processador.contexto import id_arquivo
from processador.leitura import ler_com_retentativas, ler_texto
from processador.modelos import Falha, Relatorio, Resultado

log = logging.getLogger(__name__)


def criar_pool(processos: int) -> ProcessPoolExecutor:
    """Pool de processos com o método de início 'spawn' escolhido de forma explícita.

    O fork copiaria para o filho threads em estado inconsistente (como as do asyncio.to_thread),
    e o método padrão muda conforme o sistema e a versão do Python. O spawn se comporta igual
    em todos, ao custo de iniciar cada processo importando o código de novo.
    """
    return ProcessPoolExecutor(
        max_workers=processos, mp_context=multiprocessing.get_context("spawn")
    )


async def processar_arquivo(
    caminho: Path,
    *,
    semaforo: asyncio.Semaphore,
    pool: Executor,
    timeout: float,
    dormir: Callable[[float], Awaitable[None]],
    ler: Callable[[Path], str],
) -> Resultado | Falha:
    token = id_arquivo.set(caminho.name)
    try:
        async with semaforo:
            async with asyncio.timeout(timeout):
                texto = await ler_com_retentativas(caminho, dormir=dormir, ler=ler)
        laco = asyncio.get_running_loop()
        linhas, total, por_regiao = await laco.run_in_executor(pool, agregar, texto)
        log.info("processado: %d linhas", linhas)
        return Resultado(caminho.name, linhas, total, por_regiao)
    except (OSError, TimeoutError, ValueError) as erro:
        motivo = str(erro) or type(erro).__name__
        log.error("falhou: %s", motivo)
        return Falha(caminho.name, motivo)
    finally:
        id_arquivo.reset(token)


async def processar(
    pasta: Path,
    *,
    pool: Executor,
    leituras: int = 4,
    timeout: float = 5.0,
    dormir: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ler: Callable[[Path], str] = ler_texto,
) -> Relatorio:
    """Lê vários arquivos com concorrência limitada e calcula em processos separados.

    Uma falha em um arquivo vira um registro de Falha e não derruba os demais.
    """
    semaforo = asyncio.Semaphore(leituras)
    saidas = await asyncio.gather(
        *(
            processar_arquivo(
                caminho, semaforo=semaforo, pool=pool, timeout=timeout, dormir=dormir, ler=ler
            )
            for caminho in sorted(pasta.glob("*.csv"))
        )
    )
    relatorio = Relatorio()
    for saida in saidas:
        if isinstance(saida, Resultado):
            relatorio.resultados.append(saida)
        else:
            relatorio.falhas.append(saida)
    return relatorio
