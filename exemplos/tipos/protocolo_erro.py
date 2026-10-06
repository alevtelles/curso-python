from typing import Protocol


class Fechavel(Protocol):
    def fechar(self) -> None: ...


class SemFechar:
    pass


def encerrar(recurso: Fechavel) -> None:
    recurso.fechar()


encerrar(SemFechar())
