from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class TarefaNaoFoiEncontrada(HTTPException):
    status_code: int = 404
    detail: str = "Tarefa não foi encontrada"


@dataclass
class ErroAoCriarTarefa(HTTPException):
    status_code: int = 500
    detail: str = "Erro ao criar tarefa"


@dataclass
class ErroAoAtualizarTarefa(HTTPException):
    status_code: int = 500
    detail: str = "Erro ao atualizar tarefa"


@dataclass
class ErroAoDeletarTarefa(HTTPException):
    status_code: int = 500
    detail: str = "Erro ao deletar tarefa"
