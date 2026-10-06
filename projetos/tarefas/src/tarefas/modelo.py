from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, Self


def agora_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@dataclass
class Tarefa:
    id: int
    titulo: str
    concluida: bool = False
    criada_em: str = field(default_factory=agora_iso)

    def para_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def de_dict(cls, dados: dict[str, Any]) -> Self:
        return cls(**dados)
