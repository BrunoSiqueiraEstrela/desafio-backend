from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class ValorInvalido(HTTPException):
    status_code: int = 404
    detail: str = "Email inválido"


@dataclass
class SaldoInsuficiente(HTTPException):
    status_code: int = 402
    detail: str = "Saldo insuficiente"


@dataclass
class UsuarioNaoEncontrado(HTTPException):
    status_code: int = 404
    detail: str = "Usuário não encontrado"


@dataclass
class SaldoNegativo(HTTPException):
    status_code: int = 402
    detail: str = "Saldo não pode ser negativo"


@dataclass
class DataInicialMaiorQueDataFinal(HTTPException):
    status_code: int = 400
    detail: str = "A data inicial não pode ser maior que a data final"


@dataclass
class NecessarioDataInicialEDataFinal(HTTPException):
    status_code: int = 400
    detail: str = "Necessário ter data inicial e data final ao usar o filtro de data"


@dataclass
class CarteiraNaoEncontrada(HTTPException):
    status_code: int = 404
    detail: str = "Carteira não encontrada"
