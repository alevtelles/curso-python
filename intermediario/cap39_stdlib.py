"""Capítulo 39: Biblioteca padrão essencial.

Parte: Intermediário.
Execute com: python cap39_stdlib.py
"""


# === collections e itertools ===

from collections import deque
from itertools import chain, combinations, groupby, product

ultimos = deque(maxlen=3)
for n in range(6):
    ultimos.append(n)
print(list(ultimos))

print(list(chain([1, 2], [3])))
print(list(combinations("abc", 2)))
print(list(product([0, 1], repeat=2)))

vendas = [("sul", 10), ("sul", 5), ("norte", 7)]
for regiao, itens in groupby(sorted(vendas), key=lambda v: v[0]):
    print(regiao, sum(valor for _, valor in itens))


# === json ===

import json

dados = {"nome": "Ana", "idade": 30, "tags": ["a", "b"], "ativo": True, "nota": None}
texto = json.dumps(dados, ensure_ascii=False, indent=2)
print(texto)
volta = json.loads(texto)
print(volta == dados)


# === csv ===

import csv
import io

conteudo = "produto,preco\ncaneta,3.5\ncaderno,18.9\n"
leitor = csv.DictReader(io.StringIO(conteudo))
total = sum(float(linha["preco"]) for linha in leitor)
print(round(total, 2))

saida = io.StringIO()
escritor = csv.DictWriter(saida, fieldnames=["produto", "preco"], lineterminator="\n")
escritor.writeheader()
escritor.writerow({"produto": "lápis", "preco": 1.2})
print(saida.getvalue().strip())


# === datetime e fusos horários ===

from datetime import datetime, timedelta, timezone

agora = datetime(2026, 10, 6, 14, 30, tzinfo=timezone.utc)
print(agora.isoformat())
brasilia = timezone(timedelta(hours=-3))
print(agora.astimezone(brasilia).strftime("%d/%m/%Y %H:%M"))


# === re ===

import re

texto = "Contato: ana@exemplo.com, bia@teste.org"
print(re.findall(r"[\w.]+@[\w.]+", texto))
m = re.search(r"(?P<usuario>\w+)@(?P<dominio>[\w.]+)", texto)
print(m["usuario"], m["dominio"])
print(re.sub(r"\d", "#", "tel 1234-5678"))


# === enum ===

from enum import Enum, auto


class Status(Enum):
    ABERTO = auto()
    FECHADO = auto()


print(Status.ABERTO, Status.ABERTO.name, Status["FECHADO"].value)


# === Exercício: Total por região a partir de um CSV ===

from collections import defaultdict


def total_por_regiao(texto):
    totais = defaultdict(float)
    for linha in csv.DictReader(io.StringIO(texto)):
        totais[linha["regiao"]] += float(linha["valor"])
    return dict(totais)


assert total_por_regiao("regiao,valor\nsul,10\nnorte,5\nsul,2.5\n") == {"sul": 12.5, "norte": 5.0}
print("ok")
