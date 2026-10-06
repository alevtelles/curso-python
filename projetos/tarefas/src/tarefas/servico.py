import logging

from tarefas.armazenamento import Armazenamento
from tarefas.modelo import Tarefa

log = logging.getLogger(__name__)


class TarefaNaoEncontrada(Exception):
    def __init__(self, tarefa_id: int) -> None:
        super().__init__(f"tarefa {tarefa_id} não encontrada")
        self.tarefa_id = tarefa_id


class ServicoTarefas:
    def __init__(self, armazenamento: Armazenamento) -> None:
        self._armazenamento = armazenamento

    def adicionar(self, titulo: str) -> Tarefa:
        titulo = titulo.strip()
        if not titulo:
            raise ValueError("o título não pode ser vazio")
        tarefas = self._armazenamento.carregar()
        proximo_id = max((t.id for t in tarefas), default=0) + 1
        tarefa = Tarefa(id=proximo_id, titulo=titulo)
        self._armazenamento.salvar([*tarefas, tarefa])
        log.info("tarefa %d adicionada", tarefa.id)
        return tarefa

    def listar(self, *, somente_pendentes: bool = False) -> list[Tarefa]:
        tarefas = self._armazenamento.carregar()
        return [t for t in tarefas if not t.concluida] if somente_pendentes else tarefas

    def concluir(self, tarefa_id: int) -> Tarefa:
        tarefas = self._armazenamento.carregar()
        tarefa = self._buscar(tarefas, tarefa_id)
        tarefa.concluida = True
        self._armazenamento.salvar(tarefas)
        log.info("tarefa %d concluída", tarefa_id)
        return tarefa

    def remover(self, tarefa_id: int) -> None:
        tarefas = self._armazenamento.carregar()
        tarefa = self._buscar(tarefas, tarefa_id)
        tarefas.remove(tarefa)
        self._armazenamento.salvar(tarefas)
        log.info("tarefa %d removida", tarefa_id)

    @staticmethod
    def _buscar(tarefas: list[Tarefa], tarefa_id: int) -> Tarefa:
        for tarefa in tarefas:
            if tarefa.id == tarefa_id:
                return tarefa
        raise TarefaNaoEncontrada(tarefa_id)
