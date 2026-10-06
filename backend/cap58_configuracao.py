"""Capítulo 58: Configuração profissional.

Parte: Backend.
Execute com: python cap58_configuracao.py
"""


# === Configuração tipada com pydantic-settings ===

import os
from pathlib import Path
from typing import Literal

from pydantic import SecretStr, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracao(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOJA_", extra="ignore")

    ambiente: Literal["dev", "test", "prod"] = "dev"
    porta: int = 8000
    chave_api: SecretStr

try:
    Configuracao(_env_file=None)
except ValidationError as erro:
    print([(e["loc"], e["type"]) for e in erro.errors()])

os.environ["LOJA_CHAVE_API"] = "segredo-123"
os.environ["LOJA_PORTA"] = "9000"
config = Configuracao(_env_file=None)
print(config)
print(config.porta + 1, type(config.porta).__name__)
print(config.chave_api.get_secret_value()[:7])

os.environ["LOJA_PORTA"] = "abc"
try:
    Configuracao(_env_file=None)
except ValidationError as erro:
    print(erro.errors()[0]["type"])
os.environ["LOJA_PORTA"] = "9000"


# === Quem vence: a ordem de precedência ===

Path(".env.demo").write_text("LOJA_PORTA=7000\nLOJA_AMBIENTE=test\n", encoding="utf-8")
print(Configuracao(_env_file=".env.demo").porta)
del os.environ["LOJA_PORTA"]
print(Configuracao(_env_file=".env.demo").porta)
print(Configuracao(_env_file=".env.demo", porta=1234).porta)


# === Regras de negócio sobre a configuração ===

class ConfiguracaoSegura(Configuracao):
    @model_validator(mode="after")
    def producao_exige_chave_forte(self):
        if self.ambiente == "prod" and len(self.chave_api.get_secret_value()) < 16:
            raise ValueError("em produção a chave precisa ter pelo menos 16 caracteres")
        return self


os.environ["LOJA_AMBIENTE"] = "prod"
try:
    ConfiguracaoSegura(_env_file=None)
except ValidationError as erro:
    print(erro.errors()[0]["msg"])
del os.environ["LOJA_AMBIENTE"]


# === Exercício: Um campo booleano de depuração ===

class ConfiguracaoComDebug(Configuracao):
    debug: bool = False


os.environ["LOJA_DEBUG"] = "1"
assert ConfiguracaoComDebug(_env_file=None).debug is True
os.environ["LOJA_DEBUG"] = "talvez"
try:
    ConfiguracaoComDebug(_env_file=None)
except ValidationError:
    pass
else:
    raise AssertionError("deveria recusar")
del os.environ["LOJA_DEBUG"]
print("ok")
