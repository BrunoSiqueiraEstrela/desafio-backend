from datetime import datetime
from typing import Optional
from uuid import UUID

from contexto.tarefa.dominio.objeto_de_valor.gerencia_de_tarefa import (
    OrdenarTarefa,
    StatusDaTarefa,
)

from libs.fastapi.dto import Modelo


# TODO: Add validação dos valores
class CriarTarefaEntrada(Modelo):
    titulo: str
    descricao: str
    data_de_inicio: datetime
    data_de_fim: datetime
    prioridade: int
    status: StatusDaTarefa


class SaidaTarefa(Modelo):
    id: UUID
    id_usuario: UUID

    titulo: str
    descricao: str
    data_de_inicio: datetime
    data_de_fim: datetime
    prioridade: int
    status: StatusDaTarefa
    criado_em: datetime
    atualizado_em: datetime


# TODO: Add validação dos valores
class AtualizarTarefaEntrada(Modelo):
    id: UUID
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_de_inicio: Optional[datetime] = None
    data_de_fim: Optional[datetime] = None
    prioridade: Optional[int] = None
    status: Optional[StatusDaTarefa] = None


class OrdenarTarefaPor(Modelo):
    ordenador: OrdenarTarefa
