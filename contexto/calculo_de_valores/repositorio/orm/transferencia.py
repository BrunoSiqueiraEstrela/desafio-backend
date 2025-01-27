from uuid import uuid4

from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.types import Uuid, DateTime, Enum, Integer
from sqlalchemy.sql import func
from sqlalchemy.schema import Column, Table, ForeignKeyConstraint

from contexto.calculo_de_valores.dominio.entidades.transferencia_de_valores import (
    TransferenciaDeValores,
)
from contexto.calculo_de_valores.dominio.objeto_de_valor.transferencia_de_valores import (
    StatusDeTransferencia,
)
from libs.database.config import REGISTRO_DOS_ORMS


tabela_transferencia = Table(
    "Transferencia",
    REGISTRO_DOS_ORMS.metadata,
    Column("id", Uuid(as_uuid=True), default=uuid4, primary_key=True, index=True),
    Column("id_usuario_origem", Uuid(as_uuid=True), nullable=False),
    Column("id_carteira_origem", Uuid(as_uuid=True), nullable=False),
    Column("id_usuario_destino", Uuid(as_uuid=True), nullable=False),
    Column("id_carteira_destino", Uuid(as_uuid=True), nullable=False),
    Column("valor_transferido_em_centavos", Integer(), nullable=False),
    Column("status_da_transferencia", Enum(StatusDeTransferencia), nullable=False),
    Column("transferido_em", DateTime, nullable=False),
    Column("completado_em", DateTime, nullable=True),
    Column("criado_em", DateTime, nullable=False, server_default=func.now()),  # pylint: disable=not-callable
    Column(
        "atualizado_em",
        DateTime,
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
    ),
    Column("deletado_em", DateTime, nullable=True),
    ForeignKeyConstraint(["id_usuario_origem"], ["Usuario.id"]),
    ForeignKeyConstraint(["id_carteira_origem"], ["Carteira.id"]),
    ForeignKeyConstraint(["id_usuario_destino"], ["Usuario.id"]),
    ForeignKeyConstraint(["id_carteira_destino"], ["Carteira.id"]),
)

tabela_orm_mapper: Mapper[TransferenciaDeValores] = REGISTRO_DOS_ORMS.map_imperatively(
    TransferenciaDeValores,
    tabela_transferencia,
)
