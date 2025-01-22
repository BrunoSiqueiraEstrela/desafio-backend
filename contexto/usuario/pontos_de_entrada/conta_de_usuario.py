from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends
from contexto.usuario.dominio.comandos.conta_de_usuario import (
    AtualizarNivelDeAcesso,
    CriarUsuario,
    LoginUsuario,
    ObterPerfilUsuario,
    ObterUsuario,
    ListarUsuarios,
    AtualizarUsuario,
    DeletarUsuario,
)
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from contexto.usuario.dominio.modelos.conta_de_usuario import (
    AtualizarUsuarioEntrada,
    CriarUsuarioEntrada,
    EntradaAtualizarNivelDeAcesso,
    LoginEntrada,
    SaidaUsuario,
    Token,
)

from libs.dominio.barramento import Barramento
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho
from libs.fastapi.jwt import JWTBearer
from libs.tipos.retorno import RetornoApenasId, RetornoDeDados

rota = APIRouter(tags=["usuario"])


@rota.get("/usuario/perfil/", status_code=200)
def obter_usuario_logado(
    usuario: Usuario = Depends(JWTBearer()),
) -> RetornoDeDados[SaidaUsuario]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = ObterPerfilUsuario(id_usuario=usuario.id)
    retorno_comando: Usuario = barramento.enviar_comando(comando, uow)

    return RetornoDeDados(
        dado=SaidaUsuario(
            id=retorno_comando.id,
            nome=retorno_comando.nome,
            email=retorno_comando.email,
            nivel_de_acesso=retorno_comando.nivel_de_acesso,
            criado_em=retorno_comando.criado_em,
            atualizado_em=retorno_comando.atualizado_em,
        )
    )


@rota.post("/usuario", status_code=201)
def criar_usuario(entrada: CriarUsuarioEntrada) -> RetornoApenasId[UUID]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = CriarUsuario(
        nome=entrada.nome,
        email=entrada.email,
        senha=entrada.senha,
    )
    retorno_comando: Usuario = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)


@rota.put("/usuario", status_code=200)
def atualizar_usuario(
    entrada: AtualizarUsuarioEntrada, usuario: Usuario = Depends(JWTBearer())
) -> RetornoApenasId[UUID]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = AtualizarUsuario(
        id=usuario.id,
        nome=entrada.nome,
        email=entrada.email,
        senha=entrada.senha,
    )
    retorno_comando: Usuario = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)


auth = APIRouter(tags=["auth"])


# ERRO: EMAIL ESTA CASE SENSETIVE
@auth.post("/login", status_code=200)
def login(
    entrada: LoginEntrada,
) -> RetornoDeDados[Token]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = LoginUsuario(email=entrada.email, senha=entrada.senha)

    retorno_comando: Token = barramento.enviar_comando(comando, uow)
    return RetornoDeDados(dado=retorno_comando)


# TODO: Implementar Logout
# @auth.post("/logout", status_code=200)
# def logout() -> None:
#     return None
# TODO: Implementar Refresh Token
# @auth.post("/refresh", status_code=200)
# def refresh() -> None:
#     return None

admin = APIRouter(tags=["admin"], prefix="/admin")


@admin.get("/usuario/listar-um/{id}", status_code=200)
def obter_usuario(
    id: UUID, usuario: Usuario = Depends(JWTBearer())
) -> RetornoDeDados[SaidaUsuario]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = ObterUsuario(id_usuario=id, id_admin=usuario.id)
    retorno_comando: Usuario = barramento.enviar_comando(comando, uow)

    return RetornoDeDados(
        dado=SaidaUsuario(
            id=retorno_comando.id,
            nome=retorno_comando.nome,
            email=retorno_comando.email,
            nivel_de_acesso=retorno_comando.nivel_de_acesso,
            criado_em=retorno_comando.criado_em,
            atualizado_em=retorno_comando.atualizado_em,
        )
    )


@admin.get("/usuario/listar-todos/", status_code=200)
def listar_usuarios(
    usuario: Usuario = Depends(JWTBearer()),
) -> RetornoDeDados[list[SaidaUsuario]]:
    uow = UnidadeDeTrabalho()
    barrramento = Barramento()

    comando = ListarUsuarios(id_admin=usuario.id)
    retorno_usuarios: list[Usuario] = barrramento.enviar_comando(comando, uow)

    return RetornoDeDados(
        dado=[
            SaidaUsuario(
                id=usuario.id,
                nome=usuario.nome,
                email=usuario.email,
                nivel_de_acesso=usuario.nivel_de_acesso,
                criado_em=usuario.criado_em,
                atualizado_em=usuario.atualizado_em,
            )
            for usuario in retorno_usuarios
        ]
    )


@admin.put("/usuario/nivel-de-acesso/{id}", status_code=200)
def atualizar_nivel_de_acesso(
    id: UUID,
    entrada: EntradaAtualizarNivelDeAcesso,
    usuario: Usuario = Depends(JWTBearer()),
) -> RetornoApenasId[UUID]:
    uow = UnidadeDeTrabalho()
    barrramento = Barramento()

    comando = AtualizarNivelDeAcesso(
        id_usuario=id,
        id_admin=usuario.id,
        nivel_de_acesso=entrada.nivel_de_acesso,
    )
    retorno_comando: Usuario = barrramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)


@admin.delete("/usuario/{id}", status_code=204)
def deletar_usuario(id: UUID, usuario: Usuario = Depends(JWTBearer())) -> None:
    uow = UnidadeDeTrabalho()
    barrramento = Barramento()

    comando = DeletarUsuario(id_usuario=id, id_admin=usuario.id)

    retorno_comando: Usuario = barrramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)
