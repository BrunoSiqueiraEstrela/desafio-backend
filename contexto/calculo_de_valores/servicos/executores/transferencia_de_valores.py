from contexto.calculo_de_valores.dominio.comandos.transferencia_de_valores import (
    RealizarTransferencia,
)
from contexto.calculo_de_valores.dominio.entidades.carteira import Carteira
from contexto.calculo_de_valores.dominio.entidades.transferencia_de_valores import (
    TransferenciaDeValores,
)
from contexto.calculo_de_valores.dominio.objeto_de_valor.transferencia_de_valores import (
    StatusDeTransferencia,
)
from contexto.calculo_de_valores.erros.transferencia_de_valores import (
    CarteiraNaoEncontrada,
    SaldoInsuficiente,
    SaldoNegativo,
    UsuarioNaoEncontrado,
)
from contexto.calculo_de_valores.repositorio.repo.carteira import CarteiraDeUsuarioRepo
from contexto.calculo_de_valores.repositorio.repo.transferencia_de_valores import (
    TransferenciaDeValoresRepo,
)

from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato


def realizar_transferencia(
    comando: RealizarTransferencia, uow: UnidadeDeTrabalhoAbastrato
) -> TransferenciaDeValores:
    with uow:
        repositorio_de_carteira = CarteiraDeUsuarioRepo(uow.session)
        repositorio_de_transferencia = TransferenciaDeValoresRepo(uow.session)

        carteira_origem: Carteira | None = (
            repositorio_de_carteira.obter_carteira_do_usuario(
                comando.id_usuario_origem, comando.id_carteira_origem
            )
        )

        usuario_destino: Usuario | None = (
            repositorio_de_carteira.obter_usuario_da_carteira(
                comando.id_carteira_destino
            )
        )

        if not usuario_destino:
            raise UsuarioNaoEncontrado()

        carteira_destino: Carteira | None = (
            repositorio_de_carteira.obter_carteira_do_usuario(
                usuario_destino.id, comando.id_carteira_destino
            )
        )

        if not carteira_origem or not carteira_destino:
            raise CarteiraNaoEncontrada()

        if carteira_origem.nao_tem_saldo_para_transferencia(
            valor_da_transferencia=comando.valor_transferidos_em_centavos
        ):
            raise SaldoInsuficiente()

        novo_saldo_origem: int = (
            carteira_origem.saldo_em_centavos - comando.valor_transferidos_em_centavos
        )

        if novo_saldo_origem < 0:
            raise SaldoNegativo()

        novo_saldo_destino: int = (
            carteira_destino.saldo_em_centavos + comando.valor_transferidos_em_centavos
        )

        if novo_saldo_destino < 0:
            raise SaldoNegativo()

        nova_transferencia: TransferenciaDeValores = TransferenciaDeValores.criar(
            id_usuario_origem=comando.id_usuario_origem,
            id_usuario_destino=usuario_destino.id,
            id_carteira_origem=comando.id_carteira_origem,
            id_carteira_destino=comando.id_carteira_destino,
            valor_transferido_em_centavos=comando.valor_transferidos_em_centavos,
        )

        nova_transferencia.atualizar_status(status=StatusDeTransferencia.CONCLUIDO)

        carteira_origem.atualizar_saldo(novo_saldo_origem)
        carteira_destino.atualizar_saldo(novo_saldo_destino)

        repositorio_de_carteira.atualizar_carteira(carteira_destino)
        repositorio_de_carteira.atualizar_carteira(carteira_origem)

        repositorio_de_transferencia.criar_nova_transferencia(nova_transferencia)

        uow.commit()

    return nova_transferencia
