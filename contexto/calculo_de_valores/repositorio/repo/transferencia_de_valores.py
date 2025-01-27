from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from sqlalchemy.orm.session import Session

from contexto.calculo_de_valores.dominio.entidades.transferencia_de_valores import (
    TransferenciaDeValores,
)
from libs.dominio.repositorio import Repositorio


class TransferenciaDeValoresRepoAbstrato(Repositorio, ABC):
    @abstractmethod
    def criar_nova_transferencia(self, transferencia) -> None:
        pass

    @abstractmethod
    def atualizar_transferencia(self, transferencia) -> None:
        pass

    @abstractmethod
    def listar_todas_transferencias_do_usuario(self, id_usuario) -> list:
        pass

    @abstractmethod
    def listar_todas_transferencias_do_usuario_entre_periodo_datas(
        self, id_usuario, data_inicial, data_final
    ) -> list:
        pass


class TransferenciaDeValoresRepo(TransferenciaDeValoresRepoAbstrato):
    def __init__(self, session: Session):
        self.session = session

    def criar_nova_transferencia(self, transferencia: TransferenciaDeValores) -> None:
        self.session.add(transferencia)
        return transferencia

    def atualizar_transferencia(self, transferencia: TransferenciaDeValores) -> None:
        self.session.merge(transferencia)
        return transferencia

    def listar_todas_transferencias_do_usuario(self, id_usuario: UUID) -> list:
        consulta = self.session.query(TransferenciaDeValores)
        consulta = consulta.filter(
            TransferenciaDeValores.id_usuario_origem == id_usuario,
        )
        transferencias = consulta.all()
        return transferencias

    def listar_todas_transferencias_do_usuario_entre_periodo_datas(
        self, id_usuario: UUID, data_inicial, data_final
    ) -> list:
        consulta = self.session.query(TransferenciaDeValores)
        consulta = consulta.filter(
            TransferenciaDeValores.id_usuario_origem == id_usuario,
        )
        consulta = consulta.filter(
            TransferenciaDeValores.transferido_em >= data_inicial,
        )
        consulta = consulta.filter(
            TransferenciaDeValores.transferido_em < data_final,
        )
        transferencias: List[TransferenciaDeValores] = consulta.all()
        return transferencias
