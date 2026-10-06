"""Capítulo 41: Logging e linha de comando com argparse.

Parte: Intermediário.
Execute com: python cap41_logging_cli.py
"""


# === Níveis e formato ===

import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("pedidos")
log.debug("não aparece, nível abaixo de INFO")
log.info("pedido recebido")
log.warning("estoque baixo: %d unidades", 3)


# === Um logger por módulo ===

logger = logging.getLogger(__name__)
logger.info("módulo %s", __name__)

try:
    1 / 0
except ZeroDivisionError:
    log.exception("falha ao calcular")


# === Saída estruturada ===

import json


class FormatoJson(logging.Formatter):
    def format(self, record):
        return json.dumps(
            {
                "nivel": record.levelname,
                "logger": record.name,
                "mensagem": record.getMessage(),
            },
            ensure_ascii=False,
        )


manipulador = logging.StreamHandler(sys.stdout)
manipulador.setFormatter(FormatoJson())
auditoria = logging.getLogger("auditoria")
auditoria.addHandler(manipulador)
auditoria.propagate = False
auditoria.setLevel(logging.INFO)
auditoria.info("login realizado")


# === Argumentos de linha de comando ===

import argparse


def criar_parser():
    parser = argparse.ArgumentParser(description="Saudação em linha de comando")
    parser.add_argument("nome", help="quem cumprimentar")
    parser.add_argument("--vezes", type=int, default=1, help="quantas vezes repetir")
    parser.add_argument("--gritar", action="store_true", help="usar maiúsculas")
    return parser


def main(argv=None):
    args = criar_parser().parse_args(argv)
    texto = f"Olá, {args.nome}!"
    if args.gritar:
        texto = texto.upper()
    for _ in range(args.vezes):
        print(texto)
    return 0


main(["Ana", "--vezes", "2", "--gritar"])

try:
    criar_parser().parse_args(["Ana", "--vezes", "muitas"])
except SystemExit as codigo:
    print("saiu com código", codigo.code)

def parser_com_subcomandos():
    parser = argparse.ArgumentParser(prog="tarefas")
    sub = parser.add_subparsers(dest="comando", required=True)
    adicionar = sub.add_parser("adicionar")
    adicionar.add_argument("titulo")
    sub.add_parser("listar")
    return parser


print(parser_com_subcomandos().parse_args(["adicionar", "estudar"]))


# === Exercício: Somar números pela linha de comando ===

def main_soma(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("numeros", nargs="+", type=float)
    args = parser.parse_args(argv)
    return sum(args.numeros)


assert main_soma(["1", "2.5"]) == 3.5
print("ok")
