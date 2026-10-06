"""Capítulo 47: asyncio.

Parte: Avançado.
Execute com: python cap47_assincrono.py
"""


# === Corrotinas e o laço de eventos ===

import asyncio


async def buscar(nome, atraso):
    await asyncio.sleep(atraso)
    return f"{nome} pronto"


async def principal():
    print(await buscar("a", 0.1))


asyncio.run(principal())


# === Várias tarefas ao mesmo tempo ===

async def varios():
    resultados = await asyncio.gather(
        buscar("lento", 0.3),
        buscar("rápido", 0.1),
        buscar("médio", 0.2),
    )
    print(resultados)


asyncio.run(varios())

async def por_ordem_de_chegada():
    tarefas = [buscar("lento", 0.3), buscar("rápido", 0.1), buscar("médio", 0.2)]
    for futura in asyncio.as_completed(tarefas):
        print(await futura)


asyncio.run(por_ordem_de_chegada())


# === TaskGroup e tempo limite ===

async def com_grupo():
    async with asyncio.TaskGroup() as grupo:
        t1 = grupo.create_task(buscar("x", 0.1))
        t2 = grupo.create_task(buscar("y", 0.2))
    print(t1.result(), t2.result())


async def com_timeout():
    try:
        async with asyncio.timeout(0.1):
            await buscar("demorado", 1)
    except TimeoutError:
        print("estourou o tempo")


asyncio.run(com_grupo())
asyncio.run(com_timeout())

async def falha(nome):
    await asyncio.sleep(0.05)
    raise ValueError(nome)


async def grupo_com_erros():
    try:
        async with asyncio.TaskGroup() as grupo:
            grupo.create_task(falha("a"))
            grupo.create_task(falha("b"))
    except* ValueError as grupo_de_erros:
        print(sorted(str(e) for e in grupo_de_erros.exceptions))


asyncio.run(grupo_com_erros())


# === Limitar a concorrência ===

async def limitado():
    limite = asyncio.Semaphore(2)
    ativos = 0
    maximo = 0

    async def trabalho(i):
        nonlocal ativos, maximo
        async with limite:
            ativos += 1
            maximo = max(maximo, ativos)
            await asyncio.sleep(0.05)
            ativos -= 1

    await asyncio.gather(*(trabalho(i) for i in range(6)))
    print("máximo simultâneo:", maximo)


asyncio.run(limitado())


# === O erro mais caro: bloquear o laço ===

import time


def pesado():
    time.sleep(0.2)
    return "terminou"


async def sem_bloquear():
    resultado, _ = await asyncio.gather(asyncio.to_thread(pesado), asyncio.sleep(0.05))
    print(resultado)


asyncio.run(sem_bloquear())


# === Exercício: Buscar vários com um limite ===

async def buscar_todos(nomes, limite=2):
    semaforo = asyncio.Semaphore(limite)

    async def uma(nome):
        async with semaforo:
            return nome, await buscar(nome, 0.01)

    return dict(await asyncio.gather(*(uma(n) for n in nomes)))


resultado = asyncio.run(buscar_todos(["a", "b", "c"]))
assert resultado == {"a": "a pronto", "b": "b pronto", "c": "c pronto"}
print("ok")
