from typing import Optional
from uuid import UUID
from pydantic import EmailStr

from contexto.usuario.dominio.objeto_de_valor.conta_de_usuario import NivelDeAcesso
from libs.dominio.comando import Comando


class CriarUsuario(Comando):
    nome: str
    email: EmailStr
    senha: str


class AtualizarUsuario(Comando):
    id: UUID
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None


class ObterPerfilUsuario(Comando):
    id_usuario: UUID


class ObterUsuario(Comando):
    id_admin: UUID
    id_usuario: UUID


class ListarUsuarios(Comando):
    id_admin: UUID


class DeletarUsuario(Comando):
    id_usuario: UUID
    id_admin: UUID


class LoginUsuario(Comando):
    email: EmailStr
    senha: str


class LogoutUsuario(Comando):
    token: str


class ObterUsuarioLogado(Comando):
    id_usuario: UUID


class AtualizarNivelDeAcesso(Comando):
    id_usuario: UUID
    id_admin: UUID
    nivel_de_acesso: NivelDeAcesso
