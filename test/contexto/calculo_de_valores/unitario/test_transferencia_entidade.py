from uuid import UUID, uuid4
from datetime import datetime
from contexto.calculo_de_valores.dominio.entidades.transferencia_de_valores import (
    TransferenciaDeValores,
)
from contexto.calculo_de_valores.dominio.objeto_de_valor.transferencia_de_valores import (
    StatusDeTransferencia,
)


def test_criar_transferencia_de_valores():
    id_usuario_origem: UUID = uuid4()
    id_carteira_origem: UUID = uuid4()
    id_usuario_destino: UUID = uuid4()
    id_carteira_destino: UUID = uuid4()
    valor_transferido_em_centavos = 1000

    transferencia: TransferenciaDeValores = TransferenciaDeValores.criar(
        id_usuario_origem=id_usuario_origem,
        id_carteira_origem=id_carteira_origem,
        id_usuario_destino=id_usuario_destino,
        id_carteira_destino=id_carteira_destino,
        valor_transferido_em_centavos=valor_transferido_em_centavos,
    )

    assert transferencia.id is not None
    assert transferencia.id_usuario_origem == id_usuario_origem
    assert transferencia.id_carteira_origem == id_carteira_origem
    assert transferencia.id_usuario_destino == id_usuario_destino
    assert transferencia.id_carteira_destino == id_carteira_destino
    assert transferencia.valor_transferido_em_centavos == valor_transferido_em_centavos
    assert transferencia.status_da_transferencia == StatusDeTransferencia.PENDENTE
    assert isinstance(transferencia.transferido_em, datetime)
    assert transferencia.completado_em is None


def test_atualizar_status():
    id_usuario_origem = uuid4()
    id_carteira_origem = uuid4()
    id_usuario_destino = uuid4()
    id_carteira_destino = uuid4()
    valor_transferido_em_centavos = 2000

    transferencia: TransferenciaDeValores = TransferenciaDeValores.criar(
        id_usuario_origem=id_usuario_origem,
        id_carteira_origem=id_carteira_origem,
        id_usuario_destino=id_usuario_destino,
        id_carteira_destino=id_carteira_destino,
        valor_transferido_em_centavos=valor_transferido_em_centavos,
    )

    transferencia.atualizar_status(StatusDeTransferencia.CONCLUIDO)
    assert transferencia.status_da_transferencia == StatusDeTransferencia.CONCLUIDO
