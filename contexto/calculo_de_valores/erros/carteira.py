from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class SaldoNaoPodeSerNegativo(HTTPException):
    status_code: int = 402
    detail: str = "Saldo não pode ser negativo"


@dataclass
class CarteiraNaoEncontrada(HTTPException):
    status_code: int = 404
    detail: str = "Carteira não encontrada"
