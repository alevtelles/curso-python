import argparse
import logging
from pathlib import Path

from tarefas.armazenamento import Armazenamento, ArmazenamentoJson
from tarefas.servico import ServicoTarefas, TarefaNaoEncontrada


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tarefas", description="Gerenciador de tarefas")
    parser.add_argument("--arquivo", type=Path, default=Path("tarefas.json"))
    parser.add_argument("-v", "--verboso", action="store_true", help="mostra os logs")
    sub = parser.add_subparsers(dest="comando", required=True)

    adicionar = sub.add_parser("adicionar", help="cria uma tarefa")
    adicionar.add_argument("titulo")

    listar = sub.add_parser("listar", help="mostra as tarefas")
    listar.add_argument("--pendentes", action="store_true")

    concluir = sub.add_parser("concluir", help="marca como concluída")
    concluir.add_argument("id", type=int)

    remover = sub.add_parser("remover", help="apaga uma tarefa")
    remover.add_argument("id", type=int)
    return parser


def main(argv: list[str] | None = None, armazenamento: Armazenamento | None = None) -> int:
    args = criar_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verboso else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
        force=True,
    )
    servico = ServicoTarefas(armazenamento or ArmazenamentoJson(args.arquivo))
    try:
        if args.comando == "adicionar":
            tarefa = servico.adicionar(args.titulo)
            print(f"Tarefa {tarefa.id} criada: {tarefa.titulo}")
        elif args.comando == "listar":
            tarefas = servico.listar(somente_pendentes=args.pendentes)
            if not tarefas:
                print("Nenhuma tarefa.")
            for t in tarefas:
                marca = "x" if t.concluida else " "
                print(f"[{marca}] {t.id}. {t.titulo}")
        elif args.comando == "concluir":
            print(f"Tarefa {servico.concluir(args.id).id} concluída.")
        elif args.comando == "remover":
            servico.remover(args.id)
            print(f"Tarefa {args.id} removida.")
    except (TarefaNaoEncontrada, ValueError) as erro:
        print(f"Erro: {erro}")
        return 1
    return 0
