import logging
from contextvars import ContextVar

id_arquivo: ContextVar[str] = ContextVar("id_arquivo", default="-")


class FiltroArquivo(logging.Filter):
    """Acrescenta o nome do arquivo em processamento a cada linha de log."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.arquivo = id_arquivo.get()
        return True
