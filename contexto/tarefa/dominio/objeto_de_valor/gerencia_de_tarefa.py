from enum import Enum


class StatusDaTarefa(Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"
    ATRASADO = "ATRASADO"


class OrdenarTarefa(Enum):
    TITULO = "titulo"
    PRIORIDADE = "prioridade"
    DATA_DE_INICIO = "data_de_inicio"
    DATA_DE_FIM = "data_de_fim"
    STATUS = "status"
    CRIADO_EM = "criado_em"
    ATUALIZADO_EM = "atualizado_em"
