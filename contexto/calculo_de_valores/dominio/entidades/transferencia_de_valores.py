from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from contexto.calculo_de_valores.dominio.objeto_de_valor.transferencia_de_valores import (
    StatusDeTransferencia,
)
from libs.dominio.entidade import Entidade


@dataclass
class TransferenciaDeValores(Entidade):
    id: UUID
    id_usuario_origem: UUID
    id_carteira_origem: UUID
    id_usuario_destino: UUID
    id_carteira_destino: UUID
    valor_transferido_em_centavos: int
    status_da_transferencia: int
    transferido_em: datetime
    completado_em: datetime

    @classmethod
    def criar(
        cls,
        id_usuario_origem: UUID,
        id_carteira_origem: UUID,
        id_usuario_destino: UUID,
        id_carteira_destino: UUID,
        valor_transferido_em_centavos: int,
    ) -> "TransferenciaDeValores":
        return cls(
            id=uuid4(),
            id_usuario_origem=id_usuario_origem,
            id_carteira_origem=id_carteira_origem,
            id_usuario_destino=id_usuario_destino,
            id_carteira_destino=id_carteira_destino,
            valor_transferido_em_centavos=valor_transferido_em_centavos,
            status_da_transferencia=StatusDeTransferencia.PENDENTE,
            transferido_em=datetime.now(),
            completado_em=None,
        )

    def atualizar_status(self, status: StatusDeTransferencia) -> None:
        self.status_da_transferencia = status
