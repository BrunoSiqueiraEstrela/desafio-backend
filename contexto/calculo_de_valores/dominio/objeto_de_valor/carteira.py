from contexto.calculo_de_valores.erros.carteira import SaldoNaoPodeSerNegativo
from libs.dominio.objeto_de_valor import ObjetoDeValor


class SaldoDeCarteira(ObjetoDeValor):
    saldo: int

    @classmethod
    def criar(cls, saldo: int) -> "SaldoDeCarteira":
        if saldo < 0:
            raise SaldoNaoPodeSerNegativo()

        cls.saldo = saldo

        return cls
