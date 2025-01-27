from uuid import uuid4
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    Table,
    Uuid,
    func,
)
from sqlalchemy.orm.mapper import Mapper
from libs.database.config import REGISTRO_DOS_ORMS
from contexto.calculo_de_valores.dominio.entidades.carteira import Carteira


tabela_carteira = Table(
    "Carteira",
    REGISTRO_DOS_ORMS.metadata,
    Column("id", Uuid(as_uuid=True), default=uuid4, primary_key=True, index=True),
    Column("id_usuario", Uuid(as_uuid=True), nullable=False),
    Column("saldo_em_centavos", Integer(), nullable=False),
    Column("criado_em", DateTime, nullable=False, server_default=func.now()),  # pylint: disable=not-callable
    Column(
        "atualizado_em",
        DateTime,
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
    ),
    Column("deletado_em", DateTime, nullable=True),
    ForeignKeyConstraint(["id_usuario"], ["Usuario.id"]),
)

tabela_carteira: Mapper[Carteira] = REGISTRO_DOS_ORMS.map_imperatively(
    Carteira,
    tabela_carteira,
)
