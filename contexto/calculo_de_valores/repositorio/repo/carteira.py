from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from contexto.calculo_de_valores.dominio.entidades.carteira import Carteira
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from libs.dominio.repositorio import Repositorio


class CarteiraDeUsuarioRepoAbstrato(Repositorio, ABC):
    @abstractmethod
    def obter_usuario_por_id(self, id_usuario: UUID) -> Usuario | None:
        pass

    @abstractmethod
    def listar_carteiras_do_usuario(self, id_usuario: UUID) -> list[Carteira]:
        pass

    @abstractmethod
    def obter_carteira_do_usuario(
        self, id_usuario: UUID, id_carteira: UUID
    ) -> Optional[Carteira]:
        pass

    @abstractmethod
    def obter_usuario_da_carteira(self, id_carteira: UUID) -> Usuario | None:
        pass

    @abstractmethod
    def adicionar_carteira(self, carteira_do_usuario: Carteira) -> None:
        pass

    @abstractmethod
    def atualizar_carteira(self, carteira: Carteira) -> None:
        pass


class CarteiraDeUsuarioRepo(CarteiraDeUsuarioRepoAbstrato):
    def __init__(self, session: Session):
        self.session = session

    def obter_usuario_por_id(self, id_usuario: UUID) -> Usuario | None:
        consulta = self.session.query(Usuario)
        consulta = consulta.filter_by(id=id_usuario)
        usuario = consulta.first()
        return usuario

    def obter_usuario_da_carteira(self, id_carteira: UUID) -> Usuario | None:
        consulta_carteira = self.session.query(Carteira)
        consulta_carteira = consulta_carteira.filter_by(id=id_carteira)
        carteira: Carteira | None = consulta_carteira.first()

        consulta = self.session.query(Usuario)
        consulta = consulta.filter_by(id=carteira.id_usuario)
        usuario: Usuario | None = consulta.first()
        return usuario

    def listar_carteiras_do_usuario(self, id_usuario: UUID) -> list[Carteira]:
        consulta = self.session.query(Carteira)
        consulta = consulta.filter_by(id_usuario=id_usuario)
        carteiras = consulta.all()
        return carteiras

    def obter_carteira_do_usuario(
        self, id_usuario: UUID, id_carteira: UUID
    ) -> Optional[Carteira]:
        consulta = self.session.query(Carteira)
        consulta = consulta.filter_by(id_usuario=id_usuario)
        consulta = consulta.filter_by(id=id_carteira)
        carteira = consulta.first()
        return carteira

    def adicionar_carteira(self, carteira_do_usuario: Carteira) -> None:
        self.session.add(carteira_do_usuario)

    def atualizar_carteira(self, carteira: Carteira) -> None:
        self.session.merge(carteira)
