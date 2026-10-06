"""Capítulo 46: Concorrência: GIL, threads e processos.

Parte: Avançado.
Execute com: python cap46_concorrencia.py
"""


# === Threads para I/O ===

import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def baixar(identificador):
    time.sleep(0.2)
    return f"recurso {identificador}"


def contar_primos(limite):
    total = 0
    for n in range(2, limite):
        for divisor in range(2, int(n ** 0.5) + 1):
            if n % divisor == 0:
                break
        else:
            total += 1
    return total

if __name__ == "__main__":
    inicio = time.perf_counter()
    sequencial = [baixar(i) for i in range(5)]
    t_seq = time.perf_counter() - inicio

    inicio = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as pool:
        concorrente = list(pool.map(baixar, range(5)))
    t_conc = time.perf_counter() - inicio

    print(sequencial == concorrente)
    print("threads foram mais rápidas:", t_conc < t_seq)


# === Processos para CPU ===

if __name__ == "__main__":
    limites = [20_000, 20_000, 20_000, 20_000]
    with ProcessPoolExecutor() as pool:
        resultados = list(pool.map(contar_primos, limites))
    print(resultados)


# === Estado compartilhado exige trava ===

import threading

contador = 0
trava = threading.Lock()


def incrementar(vezes):
    global contador
    for _ in range(vezes):
        with trava:
            contador += 1


if __name__ == "__main__":
    threads = [threading.Thread(target=incrementar, args=(10_000,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(contador)


# === Comunicar por fila, em vez de compartilhar ===

import queue


def produtor(fila, n):
    for i in range(n):
        fila.put(i)
    fila.put(None)


def consumidor(fila, resultados):
    while (item := fila.get()) is not None:
        resultados.append(item * item)


if __name__ == "__main__":
    fila = queue.Queue()
    resultados = []
    t1 = threading.Thread(target=produtor, args=(fila, 5))
    t2 = threading.Thread(target=consumidor, args=(fila, resultados))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(resultados)


# === Exercício: Baixar vários recursos com um limite de threads ===

def baixar_todos(ids, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(baixar, ids))


if __name__ == "__main__":
    assert baixar_todos([1, 2, 3]) == ["recurso 1", "recurso 2", "recurso 3"]
    print("ok")
