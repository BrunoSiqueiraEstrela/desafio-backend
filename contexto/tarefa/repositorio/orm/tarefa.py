from uuid import uuid4
from sqlalchemy.types import Uuid, String, DateTime, Enum, Integer
from sqlalchemy.schema import Column, Table, ForeignKeyConstraint
from sqlalchemy.sql import func

from contexto.tarefa.dominio.objeto_de_valor.gerencia_de_tarefa import StatusDaTarefa
from contexto.tarefa.dominio.entidades.gerencia_de_tarefa import Tarefa

from libs.database.config import REGISTRO_DOS_ORMS

tabela_tarefa = Table(
    "Tarefa",
    REGISTRO_DOS_ORMS.metadata,
    Column("id", Uuid(as_uuid=True), default=uuid4, primary_key=True, index=True),
    Column("id_usuario", Uuid(as_uuid=True), nullable=False, index=True),
    Column("titulo", String(100), nullable=False, index=True),
    Column("descricao", String(100), nullable=False),
    Column("data_de_inicio", DateTime, nullable=False),
    Column("data_de_fim", DateTime, nullable=False),
    Column("prioridade", Integer, nullable=False),
    Column("status", Enum(StatusDaTarefa), nullable=False),
    Column("criado_em", DateTime, nullable=False, server_default=func.now()),  #
    Column(
        "atualizado_em",
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    Column("deletado_em", DateTime, nullable=True),
    ForeignKeyConstraint(["id_usuario"], ["Usuario.id"]),
)

tabela_tarefa = REGISTRO_DOS_ORMS.map_imperatively(
    Tarefa, tabela_tarefa, properties={"id": tabela_tarefa.c.id}
)
