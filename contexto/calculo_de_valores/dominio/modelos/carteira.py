from datetime import datetime
from uuid import UUID

from pydantic import model_validator
from libs.fastapi.dto import Modelo


class CriarCarteiraEntrada(Modelo):
    saldo_em_centavos: int

    @model_validator(mode="after")
    def validacoes(cls, dados):  # pylint: disable=no-self-argument
        if dados.saldo_em_centavos < 0:
            raise ValueError("saldo não pode ser negativo")

        return dados


class AtualizarCarteiraEntrada(Modelo):
    id_carteira: UUID
    saldo_em_centavos: int

    @model_validator(mode="after")
    def validacoes(cls, dados):  # pylint: disable=no-self-argument
        if dados.saldo_em_centavos < 0:
            raise ValueError("saldo não pode ser negativo")

        return dados


class SaidaCarteira(Modelo):
    id: UUID
    saldo_em_centavos: int
    criado_em: datetime
    atualizado_em: datetime
