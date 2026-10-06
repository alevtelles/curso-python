from pathlib import Path

import pytest

from processador.cli import main


def test_gerar_e_processar(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pasta = str(tmp_path / "dados")
    assert main(["gerar", pasta, "--arquivos", "3", "--linhas", "50"]) == 0
    assert main(["processar", pasta, "--processos", "2"]) == 0
    saida = capsys.readouterr().out
    assert "arquivos processados: 3  falhas: 0" in saida
    assert "total" in saida


def test_codigo_de_saida_1_quando_ha_falha(tmp_path: Path) -> None:
    (tmp_path / "ruim.csv").write_text("x,y\n", encoding="utf-8")
    assert main(["processar", str(tmp_path), "--processos", "1"]) == 1
