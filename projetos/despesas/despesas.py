"""Gerenciador de despesas em linha de comando (projeto da parte Júnior).

Usa o que foi visto até o capítulo 25, mais o módulo json da biblioteca padrão.
Os valores ficam em centavos (inteiros), para nunca somar centavos com float.
"""

import json
from datetime import date
from pathlib import Path

ARQUIVO = Path("despesas.json")
CATEGORIAS = ["alimentação", "transporte", "moradia", "lazer", "outros"]


def carregar(caminho):
    """Lê as despesas do arquivo. Se ele ainda não existir, devolve uma lista vazia."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []


def salvar(caminho, despesas):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(despesas, arquivo, ensure_ascii=False, indent=2)


def ler_valor(texto):
    """Converte '12,50' em centavos (1250). Levanta ValueError se o valor for inválido."""
    try:
        valor = float(texto.replace(",", "."))
    except ValueError as erro:
        raise ValueError(f"valor inválido: {texto!r}") from erro
    if valor <= 0:
        raise ValueError("o valor deve ser positivo")
    return round(valor * 100)


def formatar_reais(centavos):
    reais, resto = divmod(centavos, 100)
    return f"R$ {reais:,}".replace(",", ".") + f",{resto:02d}"


def adicionar(despesas, descricao, valor_texto, categoria, data=None):
    if not descricao.strip():
        raise ValueError("a descrição não pode ser vazia")
    if categoria not in CATEGORIAS:
        raise ValueError(f"categoria inválida: {categoria!r}")
    despesa = {
        "descricao": descricao.strip(),
        "centavos": ler_valor(valor_texto),
        "categoria": categoria,
        "data": data or date.today().isoformat(),
    }
    despesas.append(despesa)
    return despesa


def remover(despesas, posicao):
    if not 1 <= posicao <= len(despesas):
        raise ValueError(f"não existe a despesa número {posicao}")
    return despesas.pop(posicao - 1)


def total_por_categoria(despesas):
    totais = {}
    for despesa in despesas:
        categoria = despesa["categoria"]
        totais[categoria] = totais.get(categoria, 0) + despesa["centavos"]
    return totais


def mostrar_lista(despesas):
    if not despesas:
        print("Nenhuma despesa registrada.")
        return
    for posicao, d in enumerate(despesas, start=1):
        print(f"{posicao}. {d['data']}  {d['descricao']:<20} {formatar_reais(d['centavos']):>12}  [{d['categoria']}]")


def mostrar_resumo(despesas):
    totais = total_por_categoria(despesas)
    for categoria in sorted(totais, key=totais.get, reverse=True):
        print(f"{categoria:<12} {formatar_reais(totais[categoria]):>12}")
    print(f"{'total':<12} {formatar_reais(sum(totais.values())):>12}")


def main():
    despesas = carregar(ARQUIVO)
    while True:
        print("\n1) Adicionar  2) Listar  3) Resumo  4) Remover  0) Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            descricao = input("Descrição: ")
            valor = input("Valor (ex.: 12,50): ")
            print("Categorias:", ", ".join(CATEGORIAS))
            categoria = input("Categoria: ").strip().lower()
            try:
                adicionar(despesas, descricao, valor, categoria)
            except ValueError as erro:
                print(f"Não foi possível adicionar: {erro}")
            else:
                salvar(ARQUIVO, despesas)
                print("Despesa registrada.")
        elif opcao == "2":
            mostrar_lista(despesas)
        elif opcao == "3":
            mostrar_resumo(despesas)
        elif opcao == "4":
            try:
                remover(despesas, int(input("Número da despesa: ")))
            except ValueError as erro:
                print(f"Não foi possível remover: {erro}")
            else:
                salvar(ARQUIVO, despesas)
                print("Despesa removida.")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
