def somar(a: float, b: float) -> float:
    return a + b


def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("divisor não pode ser zero")
    return a / b
