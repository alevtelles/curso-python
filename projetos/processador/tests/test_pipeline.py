import asyncio
import threading
import time
from pathlib import Path

from processador.cli import gerar_dados
from processador.pipeline import criar_pool, processar


def rodar(pasta: Path, **opcoes):  # type: ignore[no-untyped-def]
    async def principal():  # type: ignore[no-untyped-def]
        with criar_pool(2) as pool:
            return await processar(pasta, pool=pool, **opcoes)

    return asyncio.run(principal())


def test_processa_todos_e_soma(tmp_path: Path) -> None:
    gerar_dados(tmp_path, arquivos=3, linhas=100)
    relatorio = rodar(tmp_path)
    assert len(relatorio.resultados) == 3
    assert relatorio.falhas == []
    assert sum(r.linhas for r in relatorio.resultados) == 300


def test_arquivo_corrompido_nao_derruba_os_outros(tmp_path: Path) -> None:
    gerar_dados(tmp_path, arquivos=2, linhas=10)
    (tmp_path / "quebrado.csv").write_text("regiao,valor_centavos\nsul,abc\n", encoding="utf-8")
    relatorio = rodar(tmp_path)
    assert len(relatorio.resultados) == 2
    assert [f.arquivo for f in relatorio.falhas] == ["quebrado.csv"]
    assert "linha 2" in relatorio.falhas[0].motivo


def test_retentativas_com_espera_crescente(tmp_path: Path) -> None:
    gerar_dados(tmp_path, arquivos=1, linhas=5)
    esperas: list[float] = []
    falhas_restantes = {"n": 2}

    async def dormir_falso(segundos: float) -> None:
        esperas.append(segundos)

    def ler_instavel(caminho: Path) -> str:
        if falhas_restantes["n"] > 0:
            falhas_restantes["n"] -= 1
            raise OSError("disco ocupado")
        return caminho.read_text(encoding="utf-8")

    relatorio = rodar(tmp_path, dormir=dormir_falso, ler=ler_instavel)
    assert len(relatorio.resultados) == 1
    assert esperas == [0.1, 0.2]


def test_timeout_vira_falha(tmp_path: Path) -> None:
    gerar_dados(tmp_path, arquivos=1, linhas=5)

    def ler_lento(caminho: Path) -> str:
        time.sleep(0.3)
        return caminho.read_text(encoding="utf-8")

    relatorio = rodar(tmp_path, timeout=0.05, ler=ler_lento)
    assert relatorio.resultados == []
    assert relatorio.falhas[0].motivo == "TimeoutError"


def test_limite_de_leituras_simultaneas(tmp_path: Path) -> None:
    gerar_dados(tmp_path, arquivos=6, linhas=5)
    trava = threading.Lock()
    ativas = {"agora": 0, "maximo": 0}

    def ler_medindo(caminho: Path) -> str:
        with trava:
            ativas["agora"] += 1
            ativas["maximo"] = max(ativas["maximo"], ativas["agora"])
        time.sleep(0.05)
        with trava:
            ativas["agora"] -= 1
        return caminho.read_text(encoding="utf-8")

    rodar(tmp_path, leituras=2, ler=ler_medindo)
    assert ativas["maximo"] <= 2
