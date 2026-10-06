from pathlib import Path

import pytest

from tarefas.cli import main


def rodar(arquivo: Path, *argumentos: str) -> int:
    return main(["--arquivo", str(arquivo), *argumentos])


def test_fluxo_completo(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    arquivo = tmp_path / "t.json"
    assert rodar(arquivo, "adicionar", "Estudar Python") == 0
    assert rodar(arquivo, "adicionar", "Escrever testes") == 0
    assert rodar(arquivo, "concluir", "1") == 0
    capsys.readouterr()
    assert rodar(arquivo, "listar") == 0
    saida = capsys.readouterr().out
    assert "[x] 1. Estudar Python" in saida
    assert "[ ] 2. Escrever testes" in saida


def test_tarefa_inexistente_devolve_codigo_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert rodar(tmp_path / "t.json", "concluir", "99") == 1
    assert "Erro: tarefa 99 não encontrada" in capsys.readouterr().out


def test_argumento_invalido_sai_com_codigo_2(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as codigo:
        rodar(tmp_path / "t.json", "concluir", "abc")
    assert codigo.value.code == 2
