"""criar pedidos

Revision ID: 0001
Revises:
Create Date: 2026-10-06 15:46:53

"""

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "pedidos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cliente", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("chave_idempotencia", sa.String(length=80), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chave_idempotencia"),
    )
    op.create_index("ix_pedidos_cliente", "pedidos", ["cliente"], unique=False)
    op.create_table(
        "itens_pedido",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("produto", sa.String(length=120), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("preco_centavos", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["pedido_id"], ["pedidos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("itens_pedido")
    op.drop_index("ix_pedidos_cliente", table_name="pedidos")
    op.drop_table("pedidos")
