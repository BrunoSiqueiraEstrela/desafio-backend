from datetime import datetime
from typing import Optional
from uuid import UUID
from contexto.tarefa.dominio.objeto_de_valor.gerencia_de_tarefa import (
    OrdenarTarefa,
    StatusDaTarefa,
)
from libs.dominio.comando import Comando


class CriarTarefa(Comando):
    id_usuario: UUID
    titulo: str
    descricao: str
    data_de_inicio: datetime
    data_de_fim: datetime
    prioridade: int
    status: StatusDaTarefa


class AtualizarTarefa(Comando):
    id_tarefa: UUID
    id_usuario: UUID
    titulo: str
    descricao: str
    data_de_inicio: datetime
    data_de_fim: datetime
    prioridade: int
    status: StatusDaTarefa


class DeletarTarefa(Comando):
    id_tarefa: UUID
    id_usuario: UUID


class BuscarTarefasPorStatus(Comando):
    id_usuario: UUID
    status: list[StatusDaTarefa]


class BuscarTarefas(Comando):
    id_usuario: UUID
    status: Optional[list[StatusDaTarefa] | None]
    sort: Optional[OrdenarTarefa | None]


class BuscarTodasTarefasPorIdDoUsuario(Comando):
    id_usuario: UUID


class BuscarTarefasPorOrdemDeCriacao(Comando):
    id_usuario: UUID


class BuscarTarefaPorIdDeTarefa(Comando):
    id_usuario: UUID
    id_tarefa: UUID
