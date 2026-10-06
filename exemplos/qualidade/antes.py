import os, sys


def adicionar(item, lista=[]):
    try:
        lista.append(item)
    except:
        pass
    return lista
