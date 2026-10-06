import json
from pathlib import Path
from typing import Protocol

from tarefas.modelo import Tarefa


class Armazenamento(Protocol):
    def carregar(self) -> list[Tarefa]: ...

    def salvar(self, tarefas: list[Tarefa]) -> None: ...


class ArmazenamentoJson:
    def __init__(self, caminho: Path) -> None:
        self._caminho = caminho

    def carregar(self) -> list[Tarefa]:
        if not self._caminho.exists():
            return []
        dados = json.loads(self._caminho.read_text(encoding="utf-8"))
        return [Tarefa.de_dict(item) for item in dados]

    def salvar(self, tarefas: list[Tarefa]) -> None:
        texto = json.dumps([t.para_dict() for t in tarefas], ensure_ascii=False, indent=2)
        # Grava em um arquivo temporário e troca no final: se o programa cair no meio,
        # o arquivo original continua íntegro.
        temporario = self._caminho.with_suffix(".tmp")
        temporario.write_text(texto, encoding="utf-8")
        temporario.replace(self._caminho)


class ArmazenamentoEmMemoria:
    """Usado nos testes: não toca o disco."""

    def __init__(self) -> None:
        self._tarefas: list[Tarefa] = []

    def carregar(self) -> list[Tarefa]:
        return [Tarefa.de_dict(t.para_dict()) for t in self._tarefas]

    def salvar(self, tarefas: list[Tarefa]) -> None:
        self._tarefas = [Tarefa.de_dict(t.para_dict()) for t in tarefas]
