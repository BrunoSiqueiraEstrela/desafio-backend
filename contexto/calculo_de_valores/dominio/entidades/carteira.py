from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4, UUID

from libs.dominio.entidade import Entidade


@dataclass
class Carteira(Entidade):
    id: UUID
    id_usuario: UUID
    saldo_em_centavos: int
    criado_em: datetime
    atualizado_em: datetime
    deletado_em: datetime

    @classmethod
    def criar(cls, id_usuario: UUID, saldo_em_centavos: int) -> "Carteira":
        return cls(
            id=uuid4(),
            id_usuario=id_usuario,
            saldo_em_centavos=saldo_em_centavos,
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
            deletado_em=None,
        )

    def nao_tem_saldo_para_transferencia(self, valor_da_transferencia: int) -> None:
        if self.saldo_em_centavos < valor_da_transferencia:
            return True
        return False

    def pegar_saldo(self) -> int:
        return self.saldo_em_centavos

    def atualizar_saldo(self, saldo: int) -> None:
        self.saldo_em_centavos = saldo
        self.atualizar_atualizado_em()

    def deletar(self) -> None:
        self.deletado_em = datetime.now()
        self.atualizar_atualizado_em()

    def atualizar_atualizado_em(self):
        self.atualizado_em = datetime.now()

    def __repr__(self) -> str:
        return f"Carteira(id={self.id}, id_usuario={self.id_usuario}, saldo={self.saldo_em_centavos})"
