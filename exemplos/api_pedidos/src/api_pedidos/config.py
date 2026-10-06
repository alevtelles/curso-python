from functools import lru_cache
from typing import Literal, Self

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracao(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="API_", env_file=".env", extra="ignore")

    ambiente: Literal["dev", "test", "prod"] = "dev"
    database_url: SecretStr = SecretStr("sqlite:///./dev.db")
    log_nivel: str = "INFO"

    @model_validator(mode="after")
    def exigir_banco_de_servidor_em_producao(self) -> Self:
        if self.ambiente == "prod" and self.database_url.get_secret_value().startswith("sqlite"):
            raise ValueError("produção exige um banco de dados de servidor, não SQLite")
        return self


@lru_cache
def obter_configuracao() -> Configuracao:
    return Configuracao()
