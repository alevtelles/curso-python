"""Autoteste do gerenciador de despesas. Rode com: python testar_despesas.py"""

import tempfile
from pathlib import Path

import despesas


def testar_ler_valor():
    assert despesas.ler_valor("12,50") == 1250
    assert despesas.ler_valor("3") == 300
    for invalido in ("abc", "0", "-5"):
        try:
            despesas.ler_valor(invalido)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{invalido!r} deveria falhar")


def testar_formatar_reais():
    assert despesas.formatar_reais(1250) == "R$ 12,50"
    assert despesas.formatar_reais(123456) == "R$ 1.234,56"
    assert despesas.formatar_reais(5) == "R$ 0,05"


def testar_adicionar_e_total():
    lista = []
    despesas.adicionar(lista, "Almoço", "32,90", "alimentação", "2026-10-06")
    despesas.adicionar(lista, "Jantar", "20,00", "alimentação", "2026-10-06")
    despesas.adicionar(lista, "Ônibus", "4,50", "transporte", "2026-10-06")
    assert despesas.total_por_categoria(lista) == {"alimentação": 5290, "transporte": 450}


def testar_adicionar_recusa_dados_invalidos():
    lista = []
    for argumentos in (("", "10", "lazer"), ("Cinema", "10", "inexistente"), ("Cinema", "x", "lazer")):
        try:
            despesas.adicionar(lista, *argumentos)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{argumentos} deveria falhar")
    assert lista == []


def testar_remover():
    lista = [{"descricao": "a", "centavos": 1, "categoria": "outros", "data": "x"}]
    assert despesas.remover(lista, 1)["descricao"] == "a"
    assert lista == []
    try:
        despesas.remover(lista, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("deveria falhar")


def testar_salvar_e_carregar():
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "d.json"
        assert despesas.carregar(caminho) == []
        dados = [{"descricao": "Pão", "centavos": 850, "categoria": "alimentação", "data": "2026-10-06"}]
        despesas.salvar(caminho, dados)
        assert despesas.carregar(caminho) == dados


if __name__ == "__main__":
    testes = [nome for nome in dir() if nome.startswith("testar_") and callable(globals()[nome])]
    for nome in testes:
        globals()[nome]()
        print(f"ok  {nome}")
    print(f"{len(testes)} testes passaram")
