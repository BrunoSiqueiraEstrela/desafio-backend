from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session

from contexto.tarefa.dominio.entidades.gerencia_de_tarefa import Tarefa
from contexto.tarefa.dominio.objeto_de_valor.gerencia_de_tarefa import (
    OrdenarTarefa,
    StatusDaTarefa,
)
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario

from libs.dominio.repositorio import Repositorio
from libs.tipos.paginacao import Paginacao


class GerenciaDeTarefasRepoAbstrato(Repositorio, ABC):
    @abstractmethod
    def buscar_usuario_por_id(self, id_usuario: UUID) -> Optional[Usuario]:
        pass

    @abstractmethod
    def adicionar_tarefa(self, tarefa: Tarefa) -> Optional[Tarefa]:
        pass

    @abstractmethod
    def atualizar_tarefa(self, tarefa: Tarefa) -> Optional[Tarefa]:
        pass

    @abstractmethod
    def deletar_tarefa(self, id_tarefa: UUID) -> Optional[UUID]:
        pass

    @abstractmethod
    def buscar_tarefa_por_status(
        self, id_usuario: UUID, status: list[StatusDaTarefa]
    ) -> Optional[list[Tarefa]]:
        pass

    @abstractmethod
    def buscar_todas_tarefas_por_id_do_usuario(
        self, id_usuario: UUID
    ) -> Optional[list[Tarefa]]:
        pass

    @abstractmethod
    def buscar_tarefa_por_ordem_de_criacao(
        self, id_usuario: UUID
    ) -> Optional[list[Tarefa]]:
        pass

    @abstractmethod
    def buscar_tarefa_por_ordem_de_vencimento(
        self, id_usuario: UUID
    ) -> Optional[list[Tarefa]]:
        pass

    @abstractmethod
    def buscar_tarefa_por_ordem_de_vencimento_com_paginacao(
        self, id_usuario: UUID, paginacao: Paginacao
    ) -> Optional[list[Tarefa]]:
        pass

    @abstractmethod
    def buscar_por_id_filtrado_por_status_e_ordenado(
        self, id_usuario: UUID, status: list[StatusDaTarefa], sort: OrdenarTarefa
    ) -> Optional[list[Tarefa]]:
        pass

    @abstractmethod
    def buscar_por_id_de_usuario_e_id_de_tarefa(
        self, id_usuario: UUID, id_tarefa: UUID
    ) -> Optional[Tarefa]:
        pass


class GerenciaDeTarefasRepo(GerenciaDeTarefasRepoAbstrato):
    def __init__(self, session: Session):
        self.session = session

    def buscar_usuario_por_id(self, id_usuario: UUID) -> Optional[Usuario]:
        consulta = self.session.query(Usuario)
        consulta = consulta.filter(Usuario.id == id_usuario)
        usuario = consulta.first()
        return usuario

    def adicionar_tarefa(self, tarefa: Tarefa) -> Optional[Tarefa]:
        tarefa_adicionada = self.session.add(tarefa)
        return tarefa_adicionada

    def atualizar_tarefa(self, tarefa: Tarefa) -> Optional[Tarefa]:
        tarefa_atualizada = self.session.merge(tarefa)
        return tarefa_atualizada

    def deletar_tarefa(self, id_tarefa: UUID) -> Optional[UUID]:
        consulta = self.session.query(Tarefa)
        consulta = consulta.filter(Tarefa.id == id_tarefa)
        tarefa_id = consulta.delete()
        return tarefa_id

    def buscar_tarefa_por_status(
        self, id_usuario: UUID, status: list[StatusDaTarefa]
    ) -> Optional[list[Tarefa]]:
        consulta = self.session.query(Tarefa)
        consulta = consulta.filter(
            Tarefa.id_usuario == id_usuario, Tarefa.status.in_(status)
        )
        tarefas = consulta.all()
        return tarefas

    def buscar_todas_tarefas_por_id_do_usuario(
        self, id_usuario: UUID
    ) -> Optional[list[Tarefa]]:
        consulta = self.session.query(Tarefa)
        consulta = consulta.filter(Tarefa.id_usuario == id_usuario)
        tarefas: List[Tarefa] = consulta.all()
        return tarefas

    def buscar_tarefa_por_ordem_de_criacao(
        self, id_usuario: UUID
    ) -> Optional[list[Tarefa]]:
        consulta = self.session.query(Tarefa)
        consulta = consulta.filter(Tarefa.id_usuario == id_usuario)
        consulta = consulta.order_by(Tarefa.criado_em)
        consulta = consulta.limit(10)
        tarefas = consulta.all()
        return tarefas

    def buscar_tarefa_por_ordem_de_vencimento(
        self, id_usuario: UUID
    ) -> Optional[list[Tarefa]]:
        consulta = self.session.query(Tarefa)
        consulta = consulta.filter(Tarefa.id_usuario == id_usuario)
        consulta = consulta.order_by(Tarefa.data_de_fim)
        consulta = consulta.limit(10)
        tarefas: List[Tarefa] = consulta.all()
        return tarefas

    def buscar_tarefa_por_ordem_de_vencimento_com_paginacao(
        self, id_usuario: UUID, paginacao: Paginacao
    ) -> Optional[list[Tarefa]]:
        consulta = self.session.query(Tarefa)
        consulta = consulta.filter(Tarefa.id_usuario == id_usuario)
        consulta = consulta.order_by(Tarefa.data_de_fim)
        consulta = consulta.limit(paginacao.page_size)
        consulta = consulta.offset(paginacao.offset())
        tarefas: List[Tarefa] = consulta.all()
        return tarefas

    def buscar_por_id_filtrado_por_status_e_ordenado(
        self, id_usuario: UUID, status: list[StatusDaTarefa], sort: OrdenarTarefa
    ) -> Optional[list[Tarefa]]:
        consulta = self.session.query(Tarefa)
        consulta = consulta.filter(
            Tarefa.id_usuario == id_usuario, Tarefa.status.in_(status)
        )
        consulta = consulta.order_by(sort)
        tarefas = consulta.all()
        return tarefas

    def buscar_por_id_de_usuario_e_id_de_tarefa(
        self, id_usuario: UUID, id_tarefa: UUID
    ) -> Optional[Tarefa]:
        consulta = self.session.query(Tarefa)
        consulta = consulta.filter(
            Tarefa.id_usuario == id_usuario, Tarefa.id == id_tarefa
        )
        tarefa = consulta.first()
        return tarefa
