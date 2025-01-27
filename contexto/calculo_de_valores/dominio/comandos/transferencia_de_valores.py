from datetime import datetime

from typing import Optional
from uuid import UUID
from libs.dominio.comando import Comando


class ListarTransferenciasDeUmUsuarioPorPeriodo(Comando):
    id_usuario: UUID
    data_inicial: Optional[datetime]
    data_final: Optional[datetime]


class RealizarTransferencia(Comando):
    id_usuario_origem: UUID
    id_carteira_origem: UUID
    id_carteira_destino: UUID
    valor_transferidos_em_centavos: int
