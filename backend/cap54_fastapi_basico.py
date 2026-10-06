"""Capítulo 54: FastAPI.

Parte: Backend.
Execute com: python cap54_fastapi_basico.py
"""


# === Rotas, modelos e validação ===

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI(title="Biblioteca")


class LivroCriar(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    paginas: int = Field(gt=0)


class Livro(LivroCriar):
    id: int


banco: dict[int, Livro] = {}


@app.post("/livros", response_model=Livro, status_code=201)
def criar(dados: LivroCriar) -> Livro:
    livro = Livro(id=len(banco) + 1, **dados.model_dump())
    banco[livro.id] = livro
    return livro


@app.get("/livros/{livro_id}", response_model=Livro)
def obter(livro_id: int) -> Livro:
    if livro_id not in banco:
        raise HTTPException(status_code=404, detail="livro não encontrado")
    return banco[livro_id]


@app.get("/livros")
def listar(minimo_paginas: Annotated[int, Query(ge=0)] = 0) -> list[Livro]:
    return [livro for livro in banco.values() if livro.paginas >= minimo_paginas]


# === Testar sem subir servidor ===

cliente = TestClient(app)
print(cliente.post("/livros", json={"titulo": "Python Notes", "paginas": 500}).json())
print(cliente.get("/livros/1").status_code)
nao_existe = cliente.get("/livros/9")
print(nao_existe.status_code, nao_existe.json())

resposta = cliente.post("/livros", json={"titulo": "", "paginas": -1})
print(resposta.status_code)
print([(erro["loc"], erro["type"]) for erro in resposta.json()["detail"]])


# === Injeção de dependências ===

def obter_banco() -> dict[int, Livro]:
    return banco


BancoDep = Annotated[dict[int, Livro], Depends(obter_banco)]


@app.get("/total")
def total(base: BancoDep) -> dict[str, int]:
    return {"total": len(base)}


print(cliente.get("/total").json())

app.dependency_overrides[obter_banco] = lambda: {i: Livro(id=i, titulo="x", paginas=1) for i in range(5)}
print(cliente.get("/total").json())
app.dependency_overrides.clear()
print(sorted(app.openapi()["paths"]))


# === Exercício: Remover um livro ===

from fastapi import Response


@app.delete("/livros/{livro_id}", status_code=204)
def remover(livro_id: int) -> Response:
    if banco.pop(livro_id, None) is None:
        raise HTTPException(status_code=404, detail="livro não encontrado")
    return Response(status_code=204)


assert cliente.delete("/livros/1").status_code == 204
assert cliente.delete("/livros/1").status_code == 404
print("ok")
