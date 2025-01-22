from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends, Query

from contexto.tarefa.dominio.comandos.gerencia_de_tarefa import (
    AtualizarTarefa,
    BuscarTarefas,
    BuscarTarefaPorIdDeTarefa,
    BuscarTodasTarefasPorIdDoUsuario,
    CriarTarefa,
    DeletarTarefa,
)
from contexto.tarefa.dominio.entidades.gerencia_de_tarefa import Tarefa
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from contexto.tarefa.dominio.modelo.gerencia_de_tarefa import (
    AtualizarTarefaEntrada,
    CriarTarefaEntrada,
    SaidaTarefa,
)
from contexto.tarefa.dominio.objeto_de_valor.gerencia_de_tarefa import (
    OrdenarTarefa,
    StatusDaTarefa,
)

from libs.tipos.retorno import RetornoDeDados
from libs.fastapi.jwt import JWTBearer
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho
from libs.dominio.barramento import Barramento

rota = APIRouter(tags=["tarefa"], prefix="/tarefa")


@rota.get("/pegar-um/{id}", status_code=200)
def obter_tarefas_por_id(
    id: UUID,
    usuario: Usuario = Depends(JWTBearer()),
) -> RetornoDeDados[SaidaTarefa] | RetornoDeDados[None]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()

    comando = BuscarTarefaPorIdDeTarefa(id_usuario=usuario.id, id_tarefa=id)

    retorno_comando: Tarefa = barramento.enviar_comando(comando=comando, uow=uow)

    if retorno_comando is None:
        return RetornoDeDados(dado=None)

    return RetornoDeDados(
        dado=[
            SaidaTarefa(
                id=tarefa.id,
                id_usuario=tarefa.id_usuario,
                titulo=tarefa.titulo,
                descricao=tarefa.descricao,
                data_de_inicio=tarefa.data_de_inicio,
                data_de_fim=tarefa.data_de_fim,
                prioridade=tarefa.prioridade,
                status=tarefa.status,
                criado_em=tarefa.criado_em,
                atualizado_em=tarefa.atualizado_em,
            )
            for tarefa in retorno_comando
        ]
    )


# GET ALL
@rota.get("/suas-tarefas", status_code=200)
def obter_tarefas_por_id_do_usuario(
    usuario: Usuario = Depends(JWTBearer()),
) -> RetornoDeDados[list[SaidaTarefa]]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()
    comando = BuscarTodasTarefasPorIdDoUsuario(id_usuario=usuario.id)

    retorno_comando: list[Tarefa] = barramento.enviar_comando(comando=comando, uow=uow)

    return RetornoDeDados(
        dado=[
            SaidaTarefa(
                id=tarefa.id,
                id_usuario=tarefa.id_usuario,
                titulo=tarefa.titulo,
                descricao=tarefa.descricao,
                data_de_inicio=tarefa.data_de_inicio,
                data_de_fim=tarefa.data_de_fim,
                prioridade=tarefa.prioridade,
                status=tarefa.status,
                criado_em=tarefa.criado_em,
                atualizado_em=tarefa.atualizado_em,
            )
            for tarefa in retorno_comando
        ]
    )


# GET ALL FILTERED
@rota.get("/pesquisar", status_code=200)
def obter_tarefas_por_status(
    usuario: Usuario = Depends(JWTBearer()),
    status: list[StatusDaTarefa] | None = Query(default=None),
    sort: OrdenarTarefa | None = Query(default=None),
) -> RetornoDeDados[list[SaidaTarefa]]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()
    comando = BuscarTarefas(id_usuario=usuario.id, status=status, sort=sort)

    retorno_comando: list[Tarefa] = barramento.enviar_comando(comando=comando, uow=uow)

    return RetornoDeDados(
        dado=[
            SaidaTarefa(
                id=tarefa.id,
                id_usuario=tarefa.id_usuario,
                titulo=tarefa.titulo,
                descricao=tarefa.descricao,
                data_de_inicio=tarefa.data_de_inicio,
                data_de_fim=tarefa.data_de_fim,
                prioridade=tarefa.prioridade,
                status=tarefa.status,
                criado_em=tarefa.criado_em,
                atualizado_em=tarefa.atualizado_em,
            )
            for tarefa in retorno_comando
        ]
    )


@rota.post("/criar", status_code=201)
def criar_tarefa(
    entrada: CriarTarefaEntrada, usuario: Usuario = Depends(JWTBearer())
) -> RetornoDeDados[SaidaTarefa]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()
    comando = CriarTarefa(
        id_usuario=usuario.id,
        titulo=entrada.titulo,
        descricao=entrada.descricao,
        data_de_inicio=entrada.data_de_inicio,
        data_de_fim=entrada.data_de_fim,
        prioridade=entrada.prioridade,
        status=entrada.status,
    )

    retorno_tarefa: Tarefa = barramento.enviar_comando(comando=comando, uow=uow)

    return RetornoDeDados(
        dado=SaidaTarefa(
            id=retorno_tarefa.id,
            id_usuario=retorno_tarefa.id_usuario,
            titulo=retorno_tarefa.titulo,
            descricao=retorno_tarefa.descricao,
            data_de_inicio=retorno_tarefa.data_de_inicio,
            data_de_fim=retorno_tarefa.data_de_fim,
            prioridade=retorno_tarefa.prioridade,
            status=retorno_tarefa.status,
            criado_em=retorno_tarefa.criado_em,
            atualizado_em=retorno_tarefa.atualizado_em,
        )
    )


@rota.put("/atualizar", status_code=200)
def atualizar_tarefa(
    entrada: AtualizarTarefaEntrada, usuario: Usuario = Depends(JWTBearer())
) -> RetornoDeDados[SaidaTarefa]:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()
    comando = AtualizarTarefa(
        id_usuario=usuario.id,
        id_tarefa=entrada.id,
        titulo=entrada.titulo,
        descricao=entrada.descricao,
        data_de_inicio=entrada.data_de_inicio,
        data_de_fim=entrada.data_de_fim,
        prioridade=entrada.prioridade,
        status=entrada.status,
    )

    retorno_tarefa: Tarefa = barramento.enviar_comando(comando=comando, uow=uow)

    return RetornoDeDados(
        dado=SaidaTarefa(
            id=retorno_tarefa.id,
            id_usuario=retorno_tarefa.id_usuario,
            titulo=retorno_tarefa.titulo,
            descricao=retorno_tarefa.descricao,
            data_de_inicio=retorno_tarefa.data_de_inicio,
            data_de_fim=retorno_tarefa.data_de_fim,
            prioridade=retorno_tarefa.prioridade,
            status=retorno_tarefa.status,
            criado_em=retorno_tarefa.criado_em,
            atualizado_em=retorno_tarefa.atualizado_em,
        )
    )


@rota.delete("/deletar", status_code=200)
def deletar_tarefa(id: UUID, usuario: Usuario = Depends(JWTBearer())) -> None:
    uow = UnidadeDeTrabalho()
    barramento = Barramento()
    comando = DeletarTarefa(id_tarefa=id, id_usuario=usuario.id)
    barramento.enviar_comando(comando=comando, uow=uow)
    # Mudar para retornar id da tarefa deletada
    return None
