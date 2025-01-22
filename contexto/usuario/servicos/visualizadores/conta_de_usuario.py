from typing import Optional

from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from contexto.usuario.dominio.objeto_de_valor.conta_de_usuario import NivelDeAcesso
from contexto.usuario.erros.conta_de_usuario import ErroAoObterUsuario
from contexto.usuario.repositorio.repo.conta_de_usuario import ContaDeUsuarioRepo
from contexto.usuario.dominio.comandos.conta_de_usuario import (
    ListarUsuarios,
    ObterPerfilUsuario,
    ObterUsuario,
)

from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato


# ADMIN
def obter_usuario_por_id(
    comando: ObterUsuario, uow: UnidadeDeTrabalhoAbastrato
) -> Usuario:
    with uow:
        repositorio = ContaDeUsuarioRepo(uow.session)

        admin = repositorio.buscar_por_id(comando.id_admin)

        if not admin:
            raise ErroAoObterUsuario(detail="Usuário não encontrado", status_code=404)

        if admin.nivel_de_acesso != NivelDeAcesso.ADMINISTRADOR:
            raise ErroAoObterUsuario(detail="Usuário não autorizado", status_code=401)

        usuario: Optional[Usuario] = repositorio.buscar_por_id(comando.id)

        if not usuario:
            raise ErroAoObterUsuario(detail="Usuário não encontrado", status_code=404)

    return usuario


# TODO: ADD PAGINAÇÂO
def listar_todos_usuarios(
    comando: ListarUsuarios, uow: UnidadeDeTrabalhoAbastrato
) -> list[Usuario]:
    with uow:
        repositorio = ContaDeUsuarioRepo(uow.session)

        admin = repositorio.buscar_por_id(comando.id_admin)

        if not admin:
            raise ErroAoObterUsuario(detail="Usuário não encontrado", status_code=404)

        if admin.nivel_de_acesso != NivelDeAcesso.ADMINISTRADOR:
            raise ErroAoObterUsuario(detail="Usuário não autorizado", status_code=401)

        usuarios: list[Usuario] | None = repositorio.listar()

    return usuarios


# USUARIO
def obter_usuario_logado(
    comando: ObterPerfilUsuario, uow: UnidadeDeTrabalhoAbastrato
) -> Usuario:
    with uow:
        repositorio = ContaDeUsuarioRepo(uow.session)
        usuario: Optional[Usuario] = repositorio.buscar_por_id(comando.id_usuario)

        if not usuario:
            raise ErroAoObterUsuario(detail="Usuário não encontrado", status_code=404)

    return usuario
