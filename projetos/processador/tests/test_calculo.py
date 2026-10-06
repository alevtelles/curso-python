import pytest

from processador.calculo import agregar


def test_agrega_por_regiao() -> None:
    texto = "regiao,valor_centavos\nsul,100\nnorte,50\nsul,25\n"
    assert agregar(texto) == (3, 175, {"sul": 125, "norte": 50})


def test_cabecalho_errado_e_recusado() -> None:
    with pytest.raises(ValueError, match="cabeçalho"):
        agregar("a,b\n1,2\n")


def test_linha_invalida_informa_o_numero_da_linha() -> None:
    with pytest.raises(ValueError, match="linha 3"):
        agregar("regiao,valor_centavos\nsul,100\nsul,abc\n")
