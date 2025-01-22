from contexto.tarefa.dominio.comandos.gerencia_de_tarefa import (
    BuscarTarefaPorIdDeTarefa,
    BuscarTodasTarefasPorIdDoUsuario,
)
from contexto.tarefa.dominio.entidades.gerencia_de_tarefa import Tarefa
from contexto.tarefa.repositorio.repo.gerencia_de_tarefa import GerenciaDeTarefasRepo

from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato


def obter_tarefas_por_id(
    comando: BuscarTarefaPorIdDeTarefa, uow: UnidadeDeTrabalhoAbastrato
) -> list[Tarefa]:
    with uow:
        repositorio = GerenciaDeTarefasRepo(uow.session)

        tarefas: Tarefa | None = repositorio.buscar_por_id_de_usuario_e_id_de_tarefa(
            comando.id_usuario, comando.id_tarefa
        )

    return tarefas


def obter_tarefas_por_id_do_usuario(
    comando: BuscarTodasTarefasPorIdDoUsuario, uow: UnidadeDeTrabalhoAbastrato
) -> list[Tarefa]:
    with uow:
        repositorio = GerenciaDeTarefasRepo(uow.session)
        tarefas: list[Tarefa] | None = (
            repositorio.buscar_todas_tarefas_por_id_do_usuario(comando.id_usuario)
        )

    return tarefas


def obter_tarefas_por_ordem_de_criacao(
    comando: BuscarTodasTarefasPorIdDoUsuario, uow: UnidadeDeTrabalhoAbastrato
) -> list[Tarefa]:
    with uow:
        repositorio = GerenciaDeTarefasRepo(uow.session)
        tarefas: list[Tarefa] | None = repositorio.buscar_tarefa_por_ordem_de_criacao(
            comando.id_usuario
        )

    return tarefas


def obter_tarefas_por_ordem_de_vencimento(
    comando: BuscarTodasTarefasPorIdDoUsuario, uow: UnidadeDeTrabalhoAbastrato
) -> list[Tarefa]:
    with uow:
        repositorio = GerenciaDeTarefasRepo(uow.session)
        tarefas: list[Tarefa] | None = (
            repositorio.buscar_tarefa_por_ordem_de_vencimento(comando.id_usuario)
        )

    return tarefas


def obter_tarefas_por_status(
    comando: BuscarTodasTarefasPorIdDoUsuario, uow: UnidadeDeTrabalhoAbastrato
) -> list[Tarefa]:
    with uow:
        repositorio = GerenciaDeTarefasRepo(uow.session)
        tarefas: list[Tarefa] | None = repositorio.buscar_tarefa_por_status(
            comando.id_usuario, comando.status
        )

    return tarefas
