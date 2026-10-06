import pytest

from calc_notes import dividir, somar


def test_somar():
    assert somar(2, 3) == 5


def test_dividir_por_zero():
    with pytest.raises(ZeroDivisionError):
        dividir(1, 0)
