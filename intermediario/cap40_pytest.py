"""Capítulo 40: Testes com pytest.

Parte: Intermediário.
Execute com: python cap40_pytest.py
"""


# === O primeiro teste ===

import pytest


def eh_primo(n: int) -> bool:
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("divisor não pode ser zero")
    return a / b

def test_primo_simples():
    assert eh_primo(7)
    assert not eh_primo(8)


def test_dividir():
    assert dividir(10, 4) == 2.5


def test_dividir_por_zero():
    with pytest.raises(ZeroDivisionError, match="zero"):
        dividir(1, 0)


@pytest.mark.parametrize(
    "numero, esperado",
    [(0, False), (1, False), (2, True), (17, True), (18, False)],
)
def test_eh_primo_parametrizado(numero, esperado):
    assert eh_primo(numero) is esperado


# === Fixtures ===

@pytest.fixture
def carrinho():
    return {"itens": [], "total": 0.0}


def test_carrinho_comeca_vazio(carrinho):
    assert carrinho["itens"] == []


def test_tmp_path(tmp_path):
    arquivo = tmp_path / "dados.txt"
    arquivo.write_text("oi", encoding="utf-8")
    assert arquivo.read_text(encoding="utf-8") == "oi"


def test_capsys(capsys):
    print("olá")
    assert capsys.readouterr().out == "olá\n"

import os


def ler_ambiente():
    return os.environ.get("AMBIENTE", "desenvolvimento")


def test_ambiente_padrao(monkeypatch):
    monkeypatch.delenv("AMBIENTE", raising=False)
    assert ler_ambiente() == "desenvolvimento"


def test_ambiente_producao(monkeypatch):
    monkeypatch.setenv("AMBIENTE", "producao")
    assert ler_ambiente() == "producao"


# === Exercício: Teste uma conversão com tolerância ===

def celsius_para_fahrenheit(c):
    return c * 9 / 5 + 32


def test_conversao():
    assert celsius_para_fahrenheit(100) == 212
    assert celsius_para_fahrenheit(-40) == -40
    assert celsius_para_fahrenheit(36.6) == pytest.approx(97.88)
