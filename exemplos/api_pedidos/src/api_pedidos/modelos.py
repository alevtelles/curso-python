from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def agora() -> datetime:
    return datetime.now(UTC)


class Pedido(Base):
    __tablename__ = "pedidos"
    __table_args__ = (Index("ix_pedidos_cliente", "cliente"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(20), default="aberto")
    chave_idempotencia: Mapped[str | None] = mapped_column(String(80), unique=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)

    itens: Mapped[list["ItemPedido"]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan"
    )

    @property
    def total_centavos(self) -> int:
        return sum(item.quantidade * item.preco_centavos for item in self.itens)


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id", ondelete="CASCADE"))
    produto: Mapped[str] = mapped_column(String(120))
    quantidade: Mapped[int]
    preco_centavos: Mapped[int]

    pedido: Mapped[Pedido] = relationship(back_populates="itens")
