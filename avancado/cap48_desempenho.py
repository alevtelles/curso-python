"""Capítulo 48: Desempenho e profiling.

Parte: Avançado.
Execute com: python cap48_desempenho.py
"""


# === Medir um trecho com timeit ===

import timeit

setup = "dados = list(range(10_000)); conjunto = set(dados)"
na_lista = timeit.timeit("9_999 in dados", setup=setup, number=2_000)
no_conjunto = timeit.timeit("9_999 in conjunto", setup=setup, number=2_000)
print("conjunto mais rápido:", no_conjunto < na_lista)


# === Achar o gargalo com cProfile ===

import cProfile
import io
import pstats


def lento():
    return sum(i * i for i in range(200_000))


def principal():
    for _ in range(5):
        lento()


perfil = cProfile.Profile()
perfil.enable()
principal()
perfil.disable()

relatorio = io.StringIO()
pstats.Stats(perfil, stream=relatorio).sort_stats("cumulative").print_stats(5)
print(relatorio.getvalue())


# === O algoritmo vence a micro-otimização ===

def tem_duplicado_lento(itens):
    for i, a in enumerate(itens):
        for b in itens[i + 1:]:
            if a == b:
                return True
    return False


def tem_duplicado_rapido(itens):
    return len(set(itens)) != len(itens)


amostra = list(range(2_000))
print(tem_duplicado_lento(amostra) == tem_duplicado_rapido(amostra))

t_lento = timeit.timeit(lambda: tem_duplicado_lento(amostra), number=3)
t_rapido = timeit.timeit(lambda: tem_duplicado_rapido(amostra), number=3)
print("a versão com set é mais rápida:", t_rapido < t_lento)


# === Memória ===

import tracemalloc


def pico(funcao):
    tracemalloc.start()
    funcao()
    _, maximo = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return maximo


pico_lista = pico(lambda: sum([n for n in range(200_000)]))
pico_gerador = pico(lambda: sum(n for n in range(200_000)))
print("gerador usa menos memória:", pico_gerador < pico_lista)


# === Exercício: Interseção sem laço duplo ===

def intersecao_lenta(a, b):
    return [x for x in a if x in b]


def intersecao_rapida(a, b):
    conjunto = set(b)
    return [x for x in a if x in conjunto]


assert intersecao_rapida([1, 2, 3, 4], [3, 4, 5]) == [3, 4]
assert intersecao_rapida([1, 2, 3, 4], [3, 4, 5]) == intersecao_lenta([1, 2, 3, 4], [3, 4, 5])
print("ok")
