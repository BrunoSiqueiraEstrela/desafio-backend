from uuid import UUID
from libs.dominio.comando import Comando


class CriarCarteira(Comando):
    id_usuario: UUID
    saldo_em_centavos: int


class AtualizarCarteira(Comando):
    id_usuario: UUID
    id_carteira: UUID
    novo_saldo_em_centavos: int


class ListarCarteiras(Comando):
    id_usuario: UUID


class ObterCarteiraExpecifica(Comando):
    id_usuario: UUID
    id_carteira: UUID
