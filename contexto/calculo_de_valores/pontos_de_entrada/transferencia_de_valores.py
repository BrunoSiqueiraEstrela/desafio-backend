from datetime import datetime
from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends

from contexto.calculo_de_valores.dominio.comandos.transferencia_de_valores import (
    RealizarTransferencia,
    ListarTransferenciasDeUmUsuarioPorPeriodo,
)
from contexto.calculo_de_valores.dominio.entidades.transferencia_de_valores import (
    TransferenciaDeValores,
)
from contexto.calculo_de_valores.dominio.modelos.transferencia_de_valores import (
    SaidaTransferencia,
    TransferenciaDeValoresEntrada,
)
from contexto.calculo_de_valores.erros.transferencia_de_valores import (
    NecessarioDataInicialEDataFinal,
)
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from libs.dominio.barramento import Barramento
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho
from libs.fastapi.jwt import JWTBearer
from libs.tipos.retorno import RetornoApenasId, RetornoDeDados


rota = APIRouter(tags=["Transferencias"])


@rota.post("/transferencia", status_code=201)
def transferir_valores(
    entrada: TransferenciaDeValoresEntrada, usuario: Usuario = Depends(JWTBearer())
):
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = RealizarTransferencia(
        id_usuario_origem=usuario.id,
        id_carteira_origem=entrada.id_carteira_origem,
        id_carteira_destino=entrada.id_carteira_destino,
        valor_transferidos_em_centavos=entrada.valor_em_centavos,
    )
    retorno_comando: TransferenciaDeValores = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)


@rota.get("/transferencia/usuario/{id}", status_code=200)
def obter_transferencia(
    id: UUID,
    data_inicio: datetime | None = None,
    data_final: datetime | None = None,
) -> RetornoDeDados[list[SaidaTransferencia]]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    if not data_inicio and data_final or data_inicio and not data_final:
        raise NecessarioDataInicialEDataFinal()

    comando = ListarTransferenciasDeUmUsuarioPorPeriodo(
        id_usuario=id,
        data_inicial=data_inicio,
        data_final=data_final,
    )
    retorno_comando: list[TransferenciaDeValores] = barramento.enviar_comando(
        comando, uow
    )

    return RetornoDeDados(
        dado=[
            SaidaTransferencia(
                id=transferencia.id,
                id_usuario_origem=transferencia.id_usuario_origem,
                id_usuario_destino=transferencia.id_usuario_destino,
                id_carteira_origem=transferencia.id_carteira_origem,
                id_carteira_destino=transferencia.id_carteira_destino,
                valor_em_centavos=transferencia.valor_transferido_em_centavos,
                criado_em=transferencia.criado_em,
            )
            for transferencia in retorno_comando
        ]
    )
