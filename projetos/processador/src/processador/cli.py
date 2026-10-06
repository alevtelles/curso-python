import argparse
import asyncio
import csv
import logging
import sys
from pathlib import Path

from processador.contexto import FiltroArquivo
from processador.modelos import Relatorio
from processador.pipeline import criar_pool, processar

REGIOES = ["norte", "nordeste", "centro-oeste", "sudeste", "sul"]


def gerar_dados(pasta: Path, arquivos: int, linhas: int) -> None:
    """Gera arquivos CSV determinísticos (sem aleatoriedade, para o resultado ser repetível)."""
    pasta.mkdir(parents=True, exist_ok=True)
    for i in range(arquivos):
        with (pasta / f"vendas_{i:02d}.csv").open("w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["regiao", "valor_centavos"])
            for j in range(linhas):
                escritor.writerow([REGIOES[(i + j) % 5], (i * 7919 + j * 104729) % 50_000 + 100])


def formatar_reais(centavos: int) -> str:
    reais, resto = divmod(centavos, 100)
    return f"R$ {reais:,}".replace(",", ".") + f",{resto:02d}"


def imprimir(relatorio: Relatorio) -> None:
    print(f"arquivos processados: {len(relatorio.resultados)}  falhas: {len(relatorio.falhas)}")
    for regiao, total in sorted(relatorio.por_regiao.items()):
        print(f"  {regiao:<13}{formatar_reais(total):>16}")
    print(f"  {'total':<13}{formatar_reais(relatorio.total_centavos):>16}")
    for falha in relatorio.falhas:
        print(f"  FALHA {falha.arquivo}: {falha.motivo}")


def configurar_logs(verboso: bool) -> None:
    manipulador = logging.StreamHandler(sys.stderr)
    manipulador.addFilter(FiltroArquivo())
    manipulador.setFormatter(logging.Formatter("%(levelname)s [%(arquivo)s] %(message)s"))
    logging.basicConfig(
        level=logging.INFO if verboso else logging.WARNING, handlers=[manipulador], force=True
    )


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="processador")
    parser.add_argument("-v", "--verboso", action="store_true")
    sub = parser.add_subparsers(dest="comando", required=True)

    gerar = sub.add_parser("gerar", help="gera arquivos CSV de exemplo")
    gerar.add_argument("pasta", type=Path)
    gerar.add_argument("--arquivos", type=int, default=6)
    gerar.add_argument("--linhas", type=int, default=50_000)

    proc = sub.add_parser("processar", help="processa todos os CSV de uma pasta")
    proc.add_argument("pasta", type=Path)
    proc.add_argument("--leituras", type=int, default=4, help="leituras simultâneas")
    proc.add_argument("--processos", type=int, default=2, help="processos de cálculo")
    proc.add_argument("--timeout", type=float, default=5.0, help="segundos por arquivo")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)
    configurar_logs(args.verboso)
    if args.comando == "gerar":
        gerar_dados(args.pasta, args.arquivos, args.linhas)
        print(f"{args.arquivos} arquivos gerados em {args.pasta}")
        return 0
    with criar_pool(args.processos) as pool:
        relatorio = asyncio.run(
            processar(args.pasta, pool=pool, leituras=args.leituras, timeout=args.timeout)
        )
    imprimir(relatorio)
    return 1 if relatorio.falhas else 0
