"""Capítulo 56: SQLAlchemy.

Parte: Backend.
Execute com: python cap56_sqlalchemy_orm.py
"""


# === Modelos tipados (estilo 2.0) ===

from sqlalchemy import ForeignKey, String, create_engine, func, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
)


class Base(DeclarativeBase):
    pass


class Autor(Base):
    __tablename__ = "autores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), unique=True)
    livros: Mapped[list["Livro"]] = relationship(
        back_populates="autor", cascade="all, delete-orphan"
    )


class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(120))
    paginas: Mapped[int]
    autor_id: Mapped[int] = mapped_column(ForeignKey("autores.id"))
    autor: Mapped[Autor] = relationship(back_populates="livros")


engine = create_engine("sqlite://")
Base.metadata.create_all(engine)


# === Sessão: a unidade de trabalho ===

with Session(engine) as sessao:
    sessao.add_all([
        Autor(nome="Machado de Assis", livros=[
            Livro(titulo="Dom Casmurro", paginas=256),
            Livro(titulo="Quincas Borba", paginas=300),
        ]),
        Autor(nome="Clarice Lispector", livros=[Livro(titulo="A Hora da Estrela", paginas=88)]),
        Autor(nome="Graciliano Ramos", livros=[Livro(titulo="Vidas Secas", paginas=176)]),
    ])
    sessao.commit()


# === Consultar com select ===

with Session(engine) as sessao:
    consulta = select(Livro).where(Livro.paginas > 100).order_by(Livro.titulo)
    print([livro.titulo for livro in sessao.scalars(consulta)])
    print(sessao.scalar(select(func.sum(Livro.paginas))))
    por_autor = sessao.execute(
        select(Autor.nome, func.count(Livro.id)).join(Livro).group_by(Autor.nome).order_by(Autor.nome)
    ).all()
    print(por_autor)


# === O problema N+1 ===

from sqlalchemy import event

consultas = []
event.listen(
    engine,
    "before_cursor_execute",
    lambda conexao, cursor, comando, parametros, contexto, varias: consultas.append(comando),
)

with Session(engine) as sessao:
    consultas.clear()
    for autor in sessao.scalars(select(Autor)):
        len(autor.livros)
    print("carregamento preguiçoso:", len(consultas), "consultas")

with Session(engine) as sessao:
    consultas.clear()
    for autor in sessao.scalars(select(Autor).options(selectinload(Autor.livros))):
        len(autor.livros)
    print("com selectinload:", len(consultas), "consultas")


# === Alterar, apagar e transações ===

with Session(engine) as sessao:
    livro = sessao.scalars(select(Livro).where(Livro.titulo == "Vidas Secas")).one()
    livro.paginas = 180
    sessao.commit()
    autor = sessao.scalars(select(Autor).where(Autor.nome == "Graciliano Ramos")).one()
    sessao.delete(autor)
    sessao.commit()
    print(sessao.scalar(select(func.count(Livro.id))))

try:
    with Session(engine) as sessao, sessao.begin():
        sessao.add(Autor(nome="Machado de Assis"))
except Exception as erro:
    print(type(erro).__name__)


# === Repositório ===

class RepositorioLivros:
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def por_titulo(self, titulo: str) -> Livro | None:
        return self._sessao.scalars(select(Livro).where(Livro.titulo == titulo)).first()

    def mais_longos(self, quantidade: int) -> list[Livro]:
        consulta = select(Livro).order_by(Livro.paginas.desc()).limit(quantidade)
        return list(self._sessao.scalars(consulta))


with Session(engine) as sessao:
    repositorio = RepositorioLivros(sessao)
    print([livro.titulo for livro in repositorio.mais_longos(2)])


# === Exercício: Títulos de um autor ===

def titulos_do_autor(sessao, nome):
    consulta = select(Livro.titulo).join(Autor).where(Autor.nome == nome).order_by(Livro.titulo)
    return list(sessao.scalars(consulta))


with Session(engine) as sessao:
    assert titulos_do_autor(sessao, "Machado de Assis") == ["Dom Casmurro", "Quincas Borba"]
    assert titulos_do_autor(sessao, "Ninguém") == []
print("ok")
