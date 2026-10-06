import pytest

from tarefas.armazenamento import ArmazenamentoEmMemoria, ArmazenamentoJson
from tarefas.servico import ServicoTarefas, TarefaNaoEncontrada


@pytest.fixture
def servico() -> ServicoTarefas:
    return ServicoTarefas(ArmazenamentoEmMemoria())


def test_adicionar_gera_ids_sequenciais(servico: ServicoTarefas) -> None:
    assert servico.adicionar("a").id == 1
    assert servico.adicionar("b").id == 2


def test_titulo_vazio_e_recusado(servico: ServicoTarefas) -> None:
    with pytest.raises(ValueError, match="vazio"):
        servico.adicionar("   ")


def test_concluir_e_filtrar_pendentes(servico: ServicoTarefas) -> None:
    servico.adicionar("a")
    servico.adicionar("b")
    servico.concluir(1)
    assert [t.titulo for t in servico.listar(somente_pendentes=True)] == ["b"]
    assert len(servico.listar()) == 2


def test_remover_e_nao_reutilizar_apos_remocao_do_ultimo(servico: ServicoTarefas) -> None:
    servico.adicionar("a")
    servico.remover(1)
    assert servico.listar() == []
    with pytest.raises(TarefaNaoEncontrada):
        servico.remover(1)


def test_armazenamento_json_ida_e_volta(tmp_path) -> None:  # type: ignore[no-untyped-def]
    caminho = tmp_path / "t.json"
    ServicoTarefas(ArmazenamentoJson(caminho)).adicionar("persistida")
    outra_instancia = ServicoTarefas(ArmazenamentoJson(caminho))
    assert [t.titulo for t in outra_instancia.listar()] == ["persistida"]
    assert not caminho.with_suffix(".tmp").exists()
