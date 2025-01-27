from enum import Enum


class StatusDeTransferencia(Enum):
    PENDENTE = "PENDENTE"
    PROCESSANDO = "PROCESSANDO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"
