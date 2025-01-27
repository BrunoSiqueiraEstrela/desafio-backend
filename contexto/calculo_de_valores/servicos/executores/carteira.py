from contexto.calculo_de_valores.erros.carteira import CarteiraNaoEncontrada
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato

from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from contexto.calculo_de_valores.dominio.comandos.carteira import (
    AtualizarCarteira,
    CriarCarteira,
)
from contexto.calculo_de_valores.dominio.entidades.carteira import Carteira
from contexto.calculo_de_valores.repositorio.repo.carteira import CarteiraDeUsuarioRepo


def criar_carteira_do_usuario(
    comando: CriarCarteira, uow: UnidadeDeTrabalhoAbastrato
) -> None:
    with uow:
        repositorio = CarteiraDeUsuarioRepo(uow.session)

        usuario_da_carteira: Usuario | None = repositorio.obter_usuario_por_id(
            comando.id_usuario
        )

        if not usuario_da_carteira:
            # substituir erro por erro de dominio
            raise ValueError("Usuario não encontrado")

        carteira: Carteira = Carteira.criar(
            id_usuario=comando.id_usuario, saldo_em_centavos=comando.saldo_em_centavos
        )

        repositorio.adicionar_carteira(carteira)

        uow.commit()

    return carteira


def atualizar_carteira_do_usuario(
    comando: AtualizarCarteira, uow: UnidadeDeTrabalhoAbastrato
) -> Carteira:
    with uow:
        repositorio = CarteiraDeUsuarioRepo(uow.session)

        carteira: Carteira | None = repositorio.obter_carteira_do_usuario(
            comando.id_usuario, comando.id_carteira
        )

        if not carteira:
            # substituir erro por erro de dominio
            raise CarteiraNaoEncontrada()

        carteira.atualizar_saldo(comando.novo_saldo_em_centavos)

        uow.commit()
    return carteira
