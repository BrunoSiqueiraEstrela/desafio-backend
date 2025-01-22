from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class EmailInvalido(HTTPException):
    status_code: int = 400
    detail: str = "Email inválido"


@dataclass
class UsuarioComMesmoEmail(HTTPException):
    status_code: int = 400
    detail: str = "Já existe um usuário com esse nome"


@dataclass
class UsuarioComMesmoNome(HTTPException):
    status_code: int = 400
    detail: str = "Já existe um usuário com esse nome"


@dataclass
class ErroAoCriarUsuario(HTTPException):
    status_code: int = 500
    detail: str = "Erro ao criar usuário"


@dataclass
class ErroAoAtualizarUsuario(HTTPException):
    status_code: int = 500
    detail: str = "Erro ao atualizar usuário"


@dataclass
class ErroAoDeletarUsuario(HTTPException):
    status_code: int = 500
    detail: str = "Erro ao deletar usuário"


@dataclass
class ErroAoObterUsuario(HTTPException):
    status_code: int = 500
    detail: str = "Erro ao obter usuário"
