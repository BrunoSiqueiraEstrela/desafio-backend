from abc import abstractmethod, ABC
from uuid import UUID
from typing import Optional
from sqlalchemy.orm.session import Session

from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from libs.dominio.repositorio import Repositorio


class ContaDeUsuarioRepoAbstrato(Repositorio, ABC):
    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def buscar_por_id(self, id: UUID) -> Optional[Usuario]:
        pass

    @abstractmethod
    def listar(self) -> Optional[list[Usuario]]:
        pass

    @abstractmethod
    def salvar(self, usuario: Usuario) -> Optional[Usuario]:
        pass

    @abstractmethod
    def atualizar(self, entidade: Usuario) -> Optional[Usuario]:
        pass


class ContaDeUsuarioRepo(ContaDeUsuarioRepoAbstrato):
    def __init__(self, session: Session):
        self.session = session

    # POST
    def salvar(self, usuario: Usuario) -> Optional[Usuario]:
        usuario_salvo = self.session.add(usuario)
        return usuario_salvo

    # GET ONE
    def buscar_por_id(self, id: UUID) -> Optional[Usuario]:
        consulta = self.session.query(Usuario)
        consulta = consulta.filter(Usuario.id == id, Usuario.ativo)
        usuario = consulta.first()
        return usuario

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        consulta = self.session.query(Usuario)
        consulta = consulta.filter(Usuario.email == email, Usuario.ativo)
        usuario = consulta.first()
        return usuario

    # GET ALL
    def listar(self) -> Optional[list[Usuario]]:
        consulta = self.session.query(Usuario)
        consulta = consulta.filter(Usuario.ativo)
        usuarios = consulta.all()
        return usuarios

    # PUT
    def atualizar(self, entidade: Usuario) -> Optional[Usuario]:
        self.session.merge(entidade)
        return entidade

    # DELETE
    # def remover_por_softdelete(self, id: UUID) -> Optional[UUID]:
    # return (
    # self.session.query(Usuario)
    # .filter(Usuario.id == id)
    # .update({Usuario.deletado_em: datetime.now(), Usuario.ativo: False})
    # )
    #
    # def remover_permanentemente(self, id: UUID) -> Optional[UUID]:
    # return self.session.query(Usuario).filter(Usuario.id == id).delete()
    #
    # def ativar(self, id: UUID) -> Optional[Usuario]:
    # return (
    # self.session.query(Usuario)
    # .filter(Usuario.id == id)
    # .update({Usuario.ativo: True})
    # )
    #
