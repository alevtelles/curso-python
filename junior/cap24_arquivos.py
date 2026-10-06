"""Capítulo 24: Arquivos e pathlib.

Parte: Júnior.
Execute com: python cap24_arquivos.py
"""


# === Abrir com with ===

with open("notas.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write("primeira linha\n")
    arquivo.write("segunda linha com acentuação\n")

with open("notas.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
print(conteudo)

with open("notas.txt", "a", encoding="utf-8") as arquivo:
    arquivo.write("terceira linha\n")


# === Modos de abertura ===

try:
    with open("notas.txt", "x", encoding="utf-8") as arquivo:
        arquivo.write("não vai acontecer")
except FileExistsError:
    print("notas.txt já existe, o modo x recusou")


# === Ler linha por linha ===

with open("notas.txt", encoding="utf-8") as arquivo:
    for numero, linha in enumerate(arquivo, start=1):
        print(numero, linha.rstrip("\n"))


# === pathlib ===

from pathlib import Path

pasta = Path("saida")
pasta.mkdir(exist_ok=True)
arquivo = pasta / "relatorio.txt"
arquivo.write_text("total: 42\n", encoding="utf-8")
print(arquivo.read_text(encoding="utf-8").strip())
print(arquivo.name, arquivo.stem, arquivo.suffix, arquivo.parent)
print(arquivo.exists(), (pasta / "nao_existe.txt").exists())
for item in sorted(pasta.glob("*.txt")):
    print(item)


# === Erros comuns ===

try:
    open("nao_existe.txt", encoding="utf-8")
except FileNotFoundError as erro:
    print(erro)

base = Path(__file__).parent
print((base / "dados").name)


# === Exercício: Contar linhas e palavras ===

def estatisticas(caminho):
    linhas = palavras = 0
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            linhas += 1
            palavras += len(linha.split())
    return linhas, palavras


Path("exemplo.txt").write_text("um dois\ntrês quatro cinco\n", encoding="utf-8")
assert estatisticas("exemplo.txt") == (2, 5)
print("ok")
