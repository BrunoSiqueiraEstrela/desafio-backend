from uuid import uuid4

from contexto.calculo_de_valores.dominio.entidades.carteira import Carteira


def test_criar_carteira():
    id_usuario = uuid4()
    saldo_em_centavos = 1000
    carteira = Carteira.criar(id_usuario, saldo_em_centavos)

    assert carteira.id is not None
    assert carteira.id_usuario == id_usuario
    assert carteira.saldo_em_centavos == saldo_em_centavos
    assert carteira.criado_em is not None
    assert carteira.atualizado_em is not None
    assert carteira.deletado_em is None


def test_nao_tem_saldo_para_transferencia():
    id_usuario = uuid4()
    saldo_em_centavos = 1000
    carteira = Carteira.criar(id_usuario, saldo_em_centavos)

    assert carteira.nao_tem_saldo_para_transferencia(500) is False
    assert carteira.nao_tem_saldo_para_transferencia(1500) is True


def test_pegar_saldo():
    id_usuario = uuid4()
    saldo_em_centavos = 1000
    carteira = Carteira.criar(id_usuario, saldo_em_centavos)

    assert carteira.pegar_saldo() == saldo_em_centavos


def test_atualizar_saldo():
    id_usuario = uuid4()
    saldo_em_centavos = 1000
    carteira = Carteira.criar(id_usuario, saldo_em_centavos)

    novo_saldo = 2000
    carteira.atualizar_saldo(novo_saldo)

    assert carteira.saldo_em_centavos == novo_saldo
    assert carteira.atualizado_em is not None


def test_deletar():
    id_usuario = uuid4()
    saldo_em_centavos = 1000
    carteira = Carteira.criar(id_usuario, saldo_em_centavos)

    carteira.deletar()

    assert carteira.deletado_em is not None
    assert carteira.atualizado_em is not None
