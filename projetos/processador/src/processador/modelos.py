from dataclasses import dataclass, field


@dataclass(frozen=True)
class Resultado:
    arquivo: str
    linhas: int
    total_centavos: int
    por_regiao: dict[str, int]


@dataclass(frozen=True)
class Falha:
    arquivo: str
    motivo: str


@dataclass
class Relatorio:
    resultados: list[Resultado] = field(default_factory=list)
    falhas: list[Falha] = field(default_factory=list)

    @property
    def total_centavos(self) -> int:
        return sum(r.total_centavos for r in self.resultados)

    @property
    def por_regiao(self) -> dict[str, int]:
        totais: dict[str, int] = {}
        for resultado in self.resultados:
            for regiao, valor in resultado.por_regiao.items():
                totais[regiao] = totais.get(regiao, 0) + valor
        return totais
