import csv
import io


def agregar(texto: str) -> tuple[int, int, dict[str, int]]:
    """Etapa de CPU: roda em outro processo. Devolve (linhas, total, total por região).

    Precisa ser uma função do nível do módulo, com argumentos e retorno serializáveis,
    para poder ser enviada a um processo filho.
    """
    leitor = csv.reader(io.StringIO(texto))
    cabecalho = next(leitor, None)
    if cabecalho != ["regiao", "valor_centavos"]:
        raise ValueError(f"cabeçalho inesperado: {cabecalho}")
    linhas = total = 0
    por_regiao: dict[str, int] = {}
    for numero, linha in enumerate(leitor, start=2):
        try:
            regiao, valor_texto = linha
            valor = int(valor_texto)
        except ValueError as erro:
            raise ValueError(f"linha {numero} inválida: {linha}") from erro
        por_regiao[regiao] = por_regiao.get(regiao, 0) + valor
        total += valor
        linhas += 1
    return linhas, total, por_regiao
