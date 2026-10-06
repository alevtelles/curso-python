from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ItemCriar(BaseModel):
    produto: str = Field(min_length=1, max_length=120)
    quantidade: int = Field(gt=0, le=1000)
    preco_centavos: int = Field(gt=0)


class PedidoCriar(BaseModel):
    cliente: str = Field(min_length=1, max_length=120)
    itens: list[ItemCriar] = Field(min_length=1)


class ItemLer(ItemCriar):
    model_config = ConfigDict(from_attributes=True)


class PedidoLer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente: str
    status: Literal["aberto", "cancelado"]
    total_centavos: int
    criado_em: datetime
    itens: list[ItemLer]


class Pagina(BaseModel):
    itens: list[PedidoLer]
    proximo_cursor: int | None
