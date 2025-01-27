from datetime import datetime

from uuid import UUID
from libs.fastapi.dto import Modelo


class TransferenciaDeValoresEntrada(Modelo):
    id_carteira_origem: UUID
    id_carteira_destino: UUID
    valor_em_centavos: int

    # Validar se valor_em_centavos é positivo
    def validar(self) -> None:
        if self.valor_em_centavos <= 0:
            raise ValueError("Valor em centavos deve ser positivo")


class SaidaTransferencia(Modelo):
    id: UUID
    id_usuario_origem: UUID
    id_usuario_destino: UUID
    id_carteira_origem: UUID
    id_carteira_destino: UUID
    valor_em_centavos: int
    criado_em: datetime
