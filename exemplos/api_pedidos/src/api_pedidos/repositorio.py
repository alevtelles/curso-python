from sqlalchemy import select
from sqlalchemy.orm import Session

from api_pedidos.modelos import Pedido


class RepositorioPedidos:
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def adicionar(self, pedido: Pedido) -> Pedido:
        self._sessao.add(pedido)
        self._sessao.flush()
        return pedido

    def obter(self, pedido_id: int) -> Pedido | None:
        return self._sessao.get(Pedido, pedido_id)

    def por_chave(self, chave: str) -> Pedido | None:
        consulta = select(Pedido).where(Pedido.chave_idempotencia == chave)
        return self._sessao.scalars(consulta).first()

    def listar(self, depois_de: int, limite: int) -> list[Pedido]:
        consulta = select(Pedido).where(Pedido.id > depois_de).order_by(Pedido.id).limit(limite)
        return list(self._sessao.scalars(consulta))
