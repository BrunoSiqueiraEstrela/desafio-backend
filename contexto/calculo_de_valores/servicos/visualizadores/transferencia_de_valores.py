from contexto.calculo_de_valores.dominio.comandos.transferencia_de_valores import (
    ListarTransferenciasDeUmUsuarioPorPeriodo,
)
from contexto.calculo_de_valores.dominio.entidades.transferencia_de_valores import (
    TransferenciaDeValores,
)
from contexto.calculo_de_valores.erros.transferencia_de_valores import (
    DataInicialMaiorQueDataFinal,
)
from contexto.calculo_de_valores.repositorio.repo.transferencia_de_valores import (
    TransferenciaDeValoresRepo,
)
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato


def listar_transferencias_do_usuario(
    comando: ListarTransferenciasDeUmUsuarioPorPeriodo, uow: UnidadeDeTrabalhoAbastrato
) -> list[TransferenciaDeValores]:
    with uow:
        repositorio = TransferenciaDeValoresRepo(uow.session)

        if comando.data_inicial is None or comando.data_final is None:
            transferencias: list[TransferenciaDeValores] = (
                repositorio.listar_todas_transferencias_do_usuario(comando.id_usuario)
            )

        else:
            if comando.data_inicial > comando.data_final:
                raise DataInicialMaiorQueDataFinal()

            transferencias: list[TransferenciaDeValores] = (
                repositorio.listar_todas_transferencias_do_usuario_entre_periodo_datas(
                    comando.id_usuario, comando.data_inicial, comando.data_final
                )
            )

    return transferencias
