from datetime import datetime
from contexto.usuario.dominio.comandos.conta_de_usuario import (
    AtualizarNivelDeAcesso,
    AtualizarUsuario,
    CriarUsuario,
    DeletarUsuario,
    LoginUsuario,
)
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from contexto.usuario.dominio.modelos.conta_de_usuario import Token
from contexto.usuario.erros.conta_de_usuario import (
    ErroAoAtualizarUsuario,
    ErroAoCriarUsuario,
    ErroAoDeletarUsuario,
)
from contexto.usuario.repositorio.repo.conta_de_usuario import ContaDeUsuarioRepo
from contexto.usuario.dominio.objeto_de_valor.conta_de_usuario import NivelDeAcesso

from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato
from libs.fastapi.crypt import criar_token_de_acesso, gerar_hash_da_senha


# USUARIO
def criar_usuario(comando: CriarUsuario, uow: UnidadeDeTrabalhoAbastrato):
    usuario = Usuario.criar(
        nome=comando.nome,
        email=comando.email,
        senha=comando.senha,
        nivel_de_acesso=NivelDeAcesso.USUARIO,
    )

    with uow:
        repositorio = ContaDeUsuarioRepo(uow.session)

        email_existe = repositorio.buscar_por_email(usuario.email)

        if email_existe:
            raise ErroAoCriarUsuario(detail="Email já cadastrado", status_code=400)

        repositorio.salvar(usuario)
        uow.commit()

    return usuario


def atualizar_usuario(comando: AtualizarUsuario, uow: UnidadeDeTrabalhoAbastrato):
    if comando.senha:
        comando.senha = gerar_hash_da_senha(comando.senha)

    with uow:
        repositorio = ContaDeUsuarioRepo(uow.session)

        usuario: Usuario | None = repositorio.buscar_por_id(comando.id)

        if not usuario:
            raise ErroAoCriarUsuario(detail="Usuário não encontrado", status_code=404)

        usuario.atualizar(
            nome=comando.nome,
            email=comando.email,
            senha=comando.senha,
        )

        repositorio.atualizar(usuario)
        uow.commit()

    return usuario


# AUTH
def login_de_usuario(comando: LoginUsuario, uow: UnidadeDeTrabalhoAbastrato):
    with uow:
        repositorio = ContaDeUsuarioRepo(uow.session)

        usuario = repositorio.buscar_por_email(comando.email)

        if not usuario:
            raise ErroAoCriarUsuario(detail="Email ou senha Inválida", status_code=400)

        if not usuario.verificar_senha(comando.senha):
            raise ErroAoCriarUsuario(detail="Email ou senha Inválida", status_code=400)

    token_criado = criar_token_de_acesso({"sub": usuario.id})

    return Token(access_token=token_criado, token_type="bearer")


# ADMIN
def atualizar_nivel_de_acesso(
    comando: AtualizarNivelDeAcesso, uow: UnidadeDeTrabalhoAbastrato
):
    with uow:
        repositorio = ContaDeUsuarioRepo(uow.session)

        admin = repositorio.buscar_por_id(comando.id_admin)

        if not admin:
            raise ErroAoAtualizarUsuario(detail="Admin não encontrado", status_code=404)

        if admin.nivel_de_acesso != NivelDeAcesso.ADMINISTRADOR:
            raise ErroAoAtualizarUsuario(
                detail="Usuário não autorizado", status_code=401
            )

        usuario = repositorio.buscar_por_id(comando.id_usuario)

        if not usuario:
            raise ErroAoAtualizarUsuario(
                detail="Usuário não encontrado", status_code=404
            )

        usuario.nivel_de_acesso = comando.nivel_de_acesso

        repositorio.atualizar(usuario)
        uow.commit()

    return usuario


def deletar_usuario(
    comando: DeletarUsuario, uow: UnidadeDeTrabalhoAbastrato
) -> Usuario:
    with uow:
        repositorio = ContaDeUsuarioRepo(uow.session)

        admin: Usuario | None = repositorio.buscar_por_id(comando.id_admin)

        if not admin:
            raise ErroAoDeletarUsuario(detail="Admin não encontrado", status_code=404)

        if admin.nivel_de_acesso != NivelDeAcesso.ADMINISTRADOR:
            raise ErroAoDeletarUsuario(detail="Usuário não autorizado", status_code=401)

        usuario: Usuario | None = repositorio.buscar_por_id(comando.id_usuario)

        if usuario == admin:
            raise ErroAoDeletarUsuario(
                detail="Não é possível deletar o admin", status_code=401
            )

        if not usuario:
            raise ErroAoDeletarUsuario(detail="Usuário não encontrado", status_code=404)

        # Soft Delete
        usuario.deletado_em = datetime.now()
        usuario.desativar()

        repositorio.atualizar(comando.id_usuario)
        uow.commit()

    return usuario
