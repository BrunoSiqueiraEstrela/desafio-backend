from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import EmailStr, model_validator

from contexto.usuario.dominio.objeto_de_valor.conta_de_usuario import NivelDeAcesso
from libs.fastapi.dto import Modelo


# ENTRADAS
class CriarUsuarioEntrada(Modelo):
    nome: str
    email: EmailStr
    senha: str

    @model_validator(mode="after")
    def validacoes(cls, dados):
        if len(dados.senha) < 6:
            raise ValueError("Senha deve ter no mínimo 6 caracteres")
        if len(dados.nome) < 3:
            raise ValueError("Nome deve ter no mínimo 3 caracteres")

        return dados


class AtualizarUsuarioEntrada(Modelo):
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    senha: Optional[str] = None

    @model_validator(mode="after")
    def validacoes(cls, dados):
        if dados.senha and len(dados.senha) < 6:
            raise ValueError("Senha deve ter no mínimo 6 caracteres")

        if dados.nome and len(dados.nome) < 3:
            raise ValueError("Nome deve ter no mínimo 3 caracteres")

        if not any([dados.email, dados.nome, dados.senha]):
            raise ValueError("Nenhum dado para atualizar")

        return dados


class LoginEntrada(Modelo):
    email: EmailStr
    senha: str

    @model_validator(mode="after")
    def validacoes(cls, dados):
        # TODO: USAR
        # if dados.senha and len(dados.senha) < 6:
        # raise ValueError("Senha deve ter no mínimo 6 caracteres")
        return dados


class EntradaAtualizarNivelDeAcesso(Modelo):
    id_usuario: UUID

    nivel_de_acesso: NivelDeAcesso


class Token(Modelo):
    access_token: str
    token_type: str


class SaidaUsuario(Modelo):
    id: UUID

    nome: str
    email: EmailStr
    nivel_de_acesso: NivelDeAcesso

    criado_em: datetime
    atualizado_em: datetime
