from unittest.mock import patch
from uuid import uuid4
from contexto.calculo_de_valores.dominio.comandos.transferencia_de_valores import (
    RealizarTransferencia,
)
from contexto.calculo_de_valores.dominio.objeto_de_valor.transferencia_de_valores import (
    StatusDeTransferencia,
)
from contexto.calculo_de_valores.servicos.executores.transferencia_de_valores import (
    realizar_transferencia,
)
from contexto.calculo_de_valores.dominio.entidades.transferencia_de_valores import (
    TransferenciaDeValores,
)


from libs.dominio.barramento import Barramento

from test.contexto.mocks.repo import (
    CarteiraDeUsuarioRepoMock,
    TransferenciadeValoresRepoMock,
)
from test.contexto.mocks.uow import MockUoW


def registrar_eventos_e_comandos_mock():
    bus = Barramento()

    bus.registrar_comando(RealizarTransferencia, realizar_transferencia)


def test_realizar_transferencia_sucesso():
    registrar_eventos_e_comandos_mock()
    uow = MockUoW()
    bus = Barramento()

    comando = RealizarTransferencia(
        id_usuario_origem=uuid4(),
        id_carteira_origem=uuid4(),
        id_carteira_destino=uuid4(),
        valor_transferidos_em_centavos=1000,
    )

    with patch(
        "contexto.calculo_de_valores.servicos.executores.transferencia_de_valores.CarteiraDeUsuarioRepo",  # noqa
        CarteiraDeUsuarioRepoMock,
    ):
        with patch(
            "contexto.calculo_de_valores.servicos.executores.transferencia_de_valores.TransferenciaDeValoresRepo",  # noqa
            TransferenciadeValoresRepoMock,
        ):
            transferencia: TransferenciaDeValores = bus.enviar_comando(comando, uow)

        assert transferencia.status_da_transferencia == StatusDeTransferencia.CONCLUIDO
        assert transferencia.valor_transferido_em_centavos == 1000
        assert transferencia.id_usuario_origem == comando.id_usuario_origem
        assert transferencia.id_carteira_destino == comando.id_carteira_destino
        assert transferencia.id is not None
