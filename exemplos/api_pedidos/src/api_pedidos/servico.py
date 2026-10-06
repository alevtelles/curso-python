from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api_pedidos.esquemas import PedidoCriar
from api_pedidos.modelos import ItemPedido, Pedido
from api_pedidos.repositorio import RepositorioPedidos


class PedidoNaoEncontrado(Exception):
    def __init__(self, pedido_id: int) -> None:
        super().__init__(f"pedido {pedido_id} não encontrado")
        self.pedido_id = pedido_id


class PedidoJaCancelado(Exception):
    def __init__(self, pedido_id: int) -> None:
        super().__init__(f"pedido {pedido_id} já está cancelado")
        self.pedido_id = pedido_id


class ServicoPedidos:
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao
        self._repositorio = RepositorioPedidos(sessao)

    def criar(self, dados: PedidoCriar, chave: str | None = None) -> tuple[Pedido, bool]:
        """Devolve o pedido e um indicador de criação (False quando a chave já existia)."""
        if chave and (existente := self._repositorio.por_chave(chave)):
            return existente, False
        pedido = Pedido(
            cliente=dados.cliente,
            chave_idempotencia=chave,
            itens=[ItemPedido(**item.model_dump()) for item in dados.itens],
        )
        try:
            self._repositorio.adicionar(pedido)
            self._sessao.commit()
        except IntegrityError:
            # Duas requisições com a mesma chave podem passar pela verificação acima ao mesmo
            # tempo. Quem garante a unicidade é o banco, e aqui tratamos o erro dele.
            self._sessao.rollback()
            if chave and (existente := self._repositorio.por_chave(chave)):
                return existente, False
            raise
        return pedido, True

    def obter(self, pedido_id: int) -> Pedido:
        pedido = self._repositorio.obter(pedido_id)
        if pedido is None:
            raise PedidoNaoEncontrado(pedido_id)
        return pedido

    def cancelar(self, pedido_id: int) -> Pedido:
        pedido = self.obter(pedido_id)
        if pedido.status == "cancelado":
            raise PedidoJaCancelado(pedido_id)
        pedido.status = "cancelado"
        self._sessao.commit()
        return pedido

    def listar(self, cursor: int, limite: int) -> tuple[list[Pedido], int | None]:
        # Busca um item a mais para saber se existe próxima página.
        encontrados = self._repositorio.listar(cursor, limite + 1)
        pagina = encontrados[:limite]
        proximo = pagina[-1].id if len(encontrados) > limite else None
        return pagina, proximo
