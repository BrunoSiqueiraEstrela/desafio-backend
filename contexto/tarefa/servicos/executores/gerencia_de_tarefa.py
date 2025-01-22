from typing import Optional

from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from contexto.tarefa.dominio.comandos.gerencia_de_tarefa import (
    AtualizarTarefa,
    CriarTarefa,
    DeletarTarefa,
)
from contexto.tarefa.erros.gerencia_de_tarefa import (
    ErroAoAtualizarTarefa,
    ErroAoCriarTarefa,
    ErroAoDeletarTarefa,
)
from contexto.tarefa.dominio.entidades.gerencia_de_tarefa import Tarefa
from contexto.tarefa.repositorio.repo.gerencia_de_tarefa import GerenciaDeTarefasRepo

from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato


# TODO: Retornar ID apenas
def criar_tarefa(comando: CriarTarefa, uow: UnidadeDeTrabalhoAbastrato) -> Tarefa:
    tarefa: Tarefa = Tarefa.criar(
        id_usuario=comando.id_usuario,
        titulo=comando.titulo,
        descricao=comando.descricao,
        data_de_inicio=comando.data_de_inicio,
        data_de_fim=comando.data_de_fim,
        prioridade=comando.prioridade,
        status=comando.status,
    )

    with uow:
        repositorio = GerenciaDeTarefasRepo(uow.session)

        usuario: Usuario | None = repositorio.buscar_usuario_por_id(comando.id_usuario)

        if not usuario:
            raise ErroAoCriarTarefa(detail="Usuário não encontrado", status_code=404)

        repositorio.adicionar_tarefa(tarefa)

        uow.commit()

    return tarefa


def atualizar_tarefa(
    comando: AtualizarTarefa, uow: UnidadeDeTrabalhoAbastrato
) -> Optional[Tarefa]:
    with uow:
        repositorio = GerenciaDeTarefasRepo(uow.session)

        tarefa: Optional[Tarefa] = repositorio.buscar_por_id_de_usuario_e_id_de_tarefa(
            id_tarefa=comando.id_tarefa, id_usuario=comando.id_usuario
        )

        if not tarefa:
            raise ErroAoAtualizarTarefa(detail="Tarefa não encontrada", status_code=404)

        tarefa.atualizar(
            titulo=comando.titulo,
            descricao=comando.descricao,
            data_de_inicio=comando.data_de_inicio,
            data_de_fim=comando.data_de_fim,
            prioridade=comando.prioridade,
            status=comando.status,
        )

        repositorio.atualizar_tarefa(tarefa)

        uow.commit()

    return tarefa


# TODO: Retornar ID apenas
def deletar_tarefa(comando: DeletarTarefa, uow: UnidadeDeTrabalhoAbastrato) -> None:
    with uow:
        repo = GerenciaDeTarefasRepo(uow.session)

        tarefa: Optional[Tarefa] = repo.buscar_por_id_de_usuario_e_id_de_tarefa(
            id_tarefa=comando.id_tarefa, id_usuario=comando.id_usuario
        )
        if not tarefa:
            raise ErroAoDeletarTarefa(detail="Tarefa não encontrada", status_code=404)

        repo.deletar_tarefa(comando.id_tarefa)

        uow.commit()
