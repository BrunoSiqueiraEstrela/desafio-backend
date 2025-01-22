from uuid import UUID, uuid4
from dataclasses import dataclass
from datetime import datetime

from libs.dominio.entidade import Entidade

from contexto.tarefa.dominio.objeto_de_valor.gerencia_de_tarefa import StatusDaTarefa


@dataclass
class Tarefa(Entidade):
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

    @classmethod
    def criar(
        cls,
        id_usuario: UUID,
        titulo: str,
        descricao: str,
        data_de_inicio: datetime,
        data_de_fim: datetime,
        prioridade: int,
        status: StatusDaTarefa,
    ) -> "Tarefa":
        return cls(
            id=uuid4(),
            id_usuario=id_usuario,
            titulo=titulo,
            descricao=descricao,
            data_de_inicio=data_de_inicio,
            data_de_fim=data_de_fim,
            prioridade=prioridade,
            status=status,
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
        )

    def atualizar(
        self,
        titulo: str = None,
        descricao: str = None,
        data_de_inicio: datetime = None,
        data_de_fim: datetime = None,
        prioridade: int = None,
        status: StatusDaTarefa = None,
    ):
        if titulo:
            self.titulo = titulo
        if descricao:
            self.descricao = descricao
        if data_de_inicio:
            self.data_de_inicio = data_de_inicio
        if data_de_fim:
            self.data_de_fim = data_de_fim
        if prioridade:
            self.prioridade = prioridade

        if status:
            self.status = status

        self.atualizar_atualizado_em()

    def esta_atrasada(self):
        return self.data_de_fim < datetime.now()

    def atualizar_atualizado_em(self):
        self.atualizado_em = datetime.now()

    # def pendente(self):
    #     self.status = Status.PENDENTE
    #     self.atualizado_em = datetime.now()

    # def em_andamento(self):
    #     self.status = Status.EM_ANDAMENTO
    #     self.atualizado_em = datetime.now()

    # def concluir(self):
    #     self.status = Status.CONCLUIDA
    #     self.atualizado_em = datetime.now()

    # def atrasar(self):
    #     self.status = Status.ATRASADO
    #     self.atualizado_em = datetime.now()

    # def mudar_descricao(self, descricao: str):
    #     self.descricao = descricao
    #     self.atualizado_em = datetime.now()

    # def mudar_titulo(self, titulo: str):
    #     self.titulo = titulo
    #     self.atualizado_em = datetime.now()
