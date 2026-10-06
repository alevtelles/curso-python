"""Capítulo 55: PostgreSQL e SQL.

Parte: Backend.
Execute com: python cap55_sql.py
"""


# === Tabelas e restrições ===

import sqlite3

conexao = sqlite3.connect(":memory:")
conexao.row_factory = sqlite3.Row
conexao.execute("PRAGMA foreign_keys = ON")
conexao.executescript("""
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cidade TEXT
);
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    total_centavos INTEGER NOT NULL CHECK (total_centavos > 0)
);
INSERT INTO clientes (nome, cidade) VALUES ('Ana', 'Recife'), ('Bia', 'Natal'), ('Caio', 'Recife');
INSERT INTO pedidos (cliente_id, total_centavos) VALUES (1, 5000), (1, 2500), (2, 10000);
""")


# === Consultar: SELECT, JOIN e agregação ===

consulta = "SELECT nome FROM clientes WHERE cidade = 'Recife' ORDER BY nome"
print([linha["nome"] for linha in conexao.execute(consulta)])

juncao = """
SELECT c.nome, p.total_centavos
FROM pedidos p
JOIN clientes c ON c.id = p.cliente_id
ORDER BY p.id
"""
print([tuple(linha) for linha in conexao.execute(juncao)])

agregacao = """
SELECT c.nome, COALESCE(SUM(p.total_centavos), 0) AS total
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.nome
ORDER BY c.nome
"""
print([tuple(linha) for linha in conexao.execute(agregacao)])

com_filtro = """
SELECT cliente_id, COUNT(*) AS quantidade
FROM pedidos
GROUP BY cliente_id
HAVING COUNT(*) > 1
"""
print([tuple(linha) for linha in conexao.execute(com_filtro)])


# === Parâmetros: nunca monte SQL com texto ===

entrada = "x' OR '1'='1"
inseguro = conexao.execute(f"SELECT nome FROM clientes WHERE nome = '{entrada}'").fetchall()
seguro = conexao.execute("SELECT nome FROM clientes WHERE nome = ?", (entrada,)).fetchall()
print(len(inseguro), len(seguro))


# === Transações: tudo ou nada ===

conexao.execute("CREATE TABLE contas (id INTEGER PRIMARY KEY, saldo INTEGER NOT NULL CHECK (saldo >= 0))")
conexao.executemany("INSERT INTO contas VALUES (?, ?)", [(1, 100), (2, 50)])
conexao.commit()


def transferir(origem, destino, valor):
    with conexao:
        conexao.execute("UPDATE contas SET saldo = saldo - ? WHERE id = ?", (valor, origem))
        conexao.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor, destino))


transferir(1, 2, 30)
try:
    transferir(1, 2, 500)
except sqlite3.IntegrityError as erro:
    print("recusado:", erro)
print([tuple(linha) for linha in conexao.execute("SELECT id, saldo FROM contas ORDER BY id")])


# === Índices e o plano de consulta ===

def usa_indice(sql):
    plano = conexao.execute("EXPLAIN QUERY PLAN " + sql).fetchall()
    return any("INDEX" in linha["detail"] for linha in plano)


busca = "SELECT * FROM pedidos WHERE cliente_id = 1"
print("antes do índice:", usa_indice(busca))
conexao.execute("CREATE INDEX ix_pedidos_cliente ON pedidos (cliente_id)")
print("depois do índice:", usa_indice(busca))


# === Exercício: Total por cliente, incluindo quem não comprou ===

def total_por_cliente():
    consulta = """
        SELECT c.nome, COALESCE(SUM(p.total_centavos), 0)
        FROM clientes c
        LEFT JOIN pedidos p ON p.cliente_id = c.id
        GROUP BY c.nome
        ORDER BY c.nome
    """
    return [tuple(linha) for linha in conexao.execute(consulta)]


assert total_por_cliente() == [("Ana", 7500), ("Bia", 10000), ("Caio", 0)]
print("ok")
