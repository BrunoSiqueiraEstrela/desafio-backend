from contexto.calculo_de_valores.dominio.comandos.carteira import (
    ListarCarteiras,
    ObterCarteiraExpecifica,
)
from contexto.calculo_de_valores.dominio.entidades.carteira import Carteira
from contexto.calculo_de_valores.repositorio.repo.carteira import CarteiraDeUsuarioRepo
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato


def obter_carteira_do_usuario(
    comando: ObterCarteiraExpecifica, uow: UnidadeDeTrabalhoAbastrato
) -> Carteira | None:
    with uow:
        repositorio = CarteiraDeUsuarioRepo(uow.session)

        carteira: Carteira | None = repositorio.obter_carteira_do_usuario(
            comando.id_usuario, comando.id_carteira
        )

    return carteira


def listar_carteiras_do_usuario(
    comando: ListarCarteiras, uow: UnidadeDeTrabalhoAbastrato
) -> list[Carteira]:
    with uow:
        repositorio = CarteiraDeUsuarioRepo(uow.session)

        carteiras: list[Carteira] = repositorio.listar_carteiras_do_usuario(
            comando.id_usuario
        )

    return carteiras
