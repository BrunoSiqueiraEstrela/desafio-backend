from fastapi import APIRouter
from fastapi.params import Depends

from contexto.calculo_de_valores.dominio.comandos.carteira import (
    AtualizarCarteira,
    CriarCarteira,
    ListarCarteiras,
)
from contexto.calculo_de_valores.dominio.entidades.carteira import Carteira
from contexto.calculo_de_valores.dominio.modelos.carteira import (
    AtualizarCarteiraEntrada,
    CriarCarteiraEntrada,
    SaidaCarteira,
)
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from libs.dominio.barramento import Barramento
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho
from libs.fastapi.jwt import JWTBearer
from libs.tipos.retorno import RetornoApenasId, RetornoDeDados


rota = APIRouter(tags=["Carteiras"])


@rota.post("/carteira", status_code=201)
def criar_carteira(
    entrada: CriarCarteiraEntrada, usuario: Usuario = Depends(JWTBearer())
):
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = CriarCarteira(
        id_usuario=usuario.id, saldo_em_centavos=entrada.saldo_em_centavos
    )
    retorno_comando: Carteira = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)


@rota.get("/carteira", status_code=200)
def ver_todas_carteiras(
    usuario: Usuario = Depends(JWTBearer()),
) -> RetornoDeDados[list[SaidaCarteira]]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = ListarCarteiras(id_usuario=usuario.id)
    retorno_comando: Carteira = barramento.enviar_comando(comando, uow)

    return RetornoDeDados(
        dado=[
            SaidaCarteira(
                id=carteira.id,
                saldo_em_centavos=carteira.saldo_em_centavos,
                criado_em=carteira.criado_em,
                atualizado_em=carteira.atualizado_em,
            )
            for carteira in retorno_comando
        ]
    )


@rota.put("/carteira", status_code=200)
def atualizar_valores_da_carteira(
    entrada: AtualizarCarteiraEntrada, usuario: Usuario = Depends(JWTBearer())
):
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = AtualizarCarteira(
        id_usuario=usuario.id,
        id_carteira=entrada.id_carteira,
        novo_saldo_em_centavos=entrada.saldo_em_centavos,
    )
    retorno_comando: Carteira = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)
