from typing import Optional
from uuid import UUID
from contexto.calculo_de_valores.dominio.entidades.carteira import Carteira
from contexto.calculo_de_valores.repositorio.repo.carteira import (
    CarteiraDeUsuarioRepoAbstrato,
)
from contexto.calculo_de_valores.repositorio.repo.transferencia_de_valores import (
    TransferenciaDeValoresRepoAbstrato,
)
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from contexto.usuario.dominio.objeto_de_valor.conta_de_usuario import NivelDeAcesso


class TransferenciadeValoresRepoMock(TransferenciaDeValoresRepoAbstrato):
    def criar_nova_transferencia(self, transferencia) -> None:
        pass

    def atualizar_transferencia(self, transferencia) -> None:
        pass

    def listar_todas_transferencias_do_usuario(self, id_usuario) -> list:
        pass

    def listar_todas_transferencias_do_usuario_entre_periodo_datas(
        self, id_usuario, data_inicial, data_final
    ) -> list:
        pass


class CarteiraDeUsuarioRepoMock(CarteiraDeUsuarioRepoAbstrato):
    def __init__(self, session=None):
        self.session = session

    def obter_usuario_por_id(self, id_usuario: UUID) -> Usuario | None:
        usuario = Usuario.criar(
            nome="Usuario_Teste",
            email="example@email.com",
            senha="123456",
            nivel_de_acesso=NivelDeAcesso.USUARIO,
        )
        usuario.id = id_usuario
        return usuario

    def obter_carteira_do_usuario(
        self, id_usuario: UUID, id_carteira: UUID
    ) -> Optional[Carteira]:
        carteira = Carteira.criar(id_usuario=id_usuario, saldo_em_centavos=1000)
        carteira.id = id_carteira
        return carteira

    def obter_usuario_da_carteira(self, id_carteira: UUID) -> Usuario | None:
        usuario: Usuario = Usuario.criar(
            nome="Usuario_Teste",
            email="example@email.com",
            senha="123456",
            nivel_de_acesso=NivelDeAcesso.USUARIO,
        )
        return usuario

    def adicionar_carteira(self, carteira_do_usuario: Carteira) -> None:
        return

    def atualizar_carteira(self, carteira: Carteira) -> None:
        return

    def listar_carteiras_do_usuario(self, id_usuario: UUID) -> list[Carteira]:
        return
