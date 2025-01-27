from uuid import uuid4
from unittest.mock import patch

from test.contexto.mocks.repo import CarteiraDeUsuarioRepoMock
from test.contexto.mocks.uow import MockUoW

from contexto.calculo_de_valores.dominio.comandos.carteira import (
    CriarCarteira,
    AtualizarCarteira,
)


from contexto.calculo_de_valores.servicos.executores.carteira import (
    criar_carteira_do_usuario,
    atualizar_carteira_do_usuario,
)
from libs.dominio.barramento import Barramento


def registrar_eventos_e_comandos_mock():
    bus = Barramento()

    bus.registrar_comando(CriarCarteira, criar_carteira_do_usuario)
    bus.registrar_comando(AtualizarCarteira, atualizar_carteira_do_usuario)


def test_criar_carteira_do_usuario():
    registrar_eventos_e_comandos_mock()
    uow = MockUoW()
    bus = Barramento()

    comando = CriarCarteira(id_usuario=uuid4(), saldo_em_centavos=1000)

    with patch(
        "contexto.calculo_de_valores.servicos.executores.carteira.CarteiraDeUsuarioRepo",
        CarteiraDeUsuarioRepoMock,
    ):
        carteira = bus.enviar_comando(comando, uow)

        assert carteira.saldo_em_centavos == comando.saldo_em_centavos
        assert carteira.id_usuario == comando.id_usuario


def test_atualizar_carteira_do_usuario():
    registrar_eventos_e_comandos_mock()
    uow = MockUoW()
    bus = Barramento()

    comando = AtualizarCarteira(
        id_usuario=uuid4(), id_carteira=uuid4(), novo_saldo_em_centavos=2000
    )

    with patch(
        "contexto.calculo_de_valores.servicos.executores.carteira.CarteiraDeUsuarioRepo",
        CarteiraDeUsuarioRepoMock,
    ):
        carteira_atualizada = bus.enviar_comando(comando, uow)

        assert carteira_atualizada.id == comando.id_carteira
        assert carteira_atualizada.saldo_em_centavos == comando.novo_saldo_em_centavos
