import argparse

from calc_notes.operacoes import somar


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="calc-notes")
    parser.add_argument("a", type=float)
    parser.add_argument("b", type=float)
    args = parser.parse_args(argv)
    print(somar(args.a, args.b))
    return 0
