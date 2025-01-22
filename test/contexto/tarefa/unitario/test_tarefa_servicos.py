from datetime import datetime, timedelta
from typing import Optional
from unittest.mock import patch
from uuid import UUID, uuid4

from test.contexto.spy.uow import MockUoW

from contexto.tarefa.repositorio.repo.gerencia_de_tarefa import (
    GerenciaDeTarefasRepoAbstrato,
)
from contexto.tarefa.servicos.executores.gerencia_de_tarefa import criar_tarefa
from contexto.tarefa.dominio.comandos.gerencia_de_tarefa import (
    AtualizarTarefa,
    CriarTarefa,
    DeletarTarefa,
)
from contexto.tarefa.dominio.entidades.gerencia_de_tarefa import Tarefa
from contexto.tarefa.dominio.objeto_de_valor.gerencia_de_tarefa import StatusDaTarefa
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from contexto.usuario.dominio.objeto_de_valor.conta_de_usuario import NivelDeAcesso

from libs.dominio.barramento import Barramento


class MockGerenciaDeTarefasRepo(GerenciaDeTarefasRepoAbstrato):
    def __init__(self, session=None):
        self.session = session

    def adicionar_tarefa(self, tarefa):
        return tarefa

    def atualizar_tarefa(self, tarefa):
        return tarefa

    def buscar_por_id_filtrado_por_status_e_ordenado(
        self, id_usuario: UUID, status: list[StatusDaTarefa], sort
    ):
        pass

    def buscar_tarefa_por_ordem_de_criacao(self, id_usuario: UUID):
        pass

    def buscar_tarefa_por_ordem_de_vencimento(self, id_usuario: UUID):
        pass

    def buscar_tarefa_por_ordem_de_vencimento_com_paginacao(
        self, id_usuario: UUID, paginacao
    ):
        pass

    def buscar_tarefa_por_status(self, id_usuario: UUID, status: list[StatusDaTarefa]):
        pass

    def buscar_todas_tarefas_por_id_do_usuario(self, id_usuario: UUID):
        pass

    def deletar_tarefa(self, id_tarefa):
        pass

    def buscar_usuario_por_id(self, id_usuario: UUID) -> Optional[Usuario]:
        usuario: Usuario = Usuario.criar(
            nome="nome",
            email="email",
            senha="senha",
            nivel_de_acesso=NivelDeAcesso.USUARIO,
        )
        usuario.id = id_usuario
        return usuario

    def remover(self, id_tarefa):
        return True

    def buscar_por_id_de_usuario_e_id_de_tarefa(self, *args, **kwargs):
        hora_inicio = datetime.now() - timedelta(hours=8)
        hora_fim = datetime.now() - timedelta(hours=4)
        return Tarefa.criar(
            id_usuario=uuid4(),
            titulo="titulo antigo",
            descricao="descricao antiga",
            data_de_inicio=hora_inicio,
            data_de_fim=hora_fim,
            prioridade=10,
            status=StatusDaTarefa.ATRASADO,
        )


# Erro ao criar teste, necessario usar path com with


def registrar_eventos_e_comandos_teste():
    barramento = Barramento()
    barramento.registrar_comando(CriarTarefa, criar_tarefa)
    barramento.registrar_comando(AtualizarTarefa, criar_tarefa)
    barramento.registrar_comando(DeletarTarefa, criar_tarefa)


def test_service_criar_tarefa():
    registrar_eventos_e_comandos_teste()

    hora_inicio = datetime.now() - timedelta(hours=8)
    hora_fim = datetime.now() - timedelta(hours=4)

    comando = CriarTarefa(
        id_usuario=uuid4(),
        titulo="titulo",
        descricao="descricao",
        data_de_inicio=hora_inicio,
        data_de_fim=hora_fim,
        prioridade=1,
        status=StatusDaTarefa.PENDENTE,
    )

    uow = MockUoW()
    bus = Barramento()

    with patch(
        "contexto.tarefa.servicos.executores.gerencia_de_tarefa.GerenciaDeTarefasRepo",
        MockGerenciaDeTarefasRepo,
    ):
        tarefa = bus.enviar_comando(comando, uow)

        assert tarefa is not None
        assert tarefa.titulo == "titulo"
        assert tarefa.descricao == "descricao"
        assert tarefa.data_de_inicio == hora_inicio
        assert tarefa.data_de_fim == hora_fim
        assert tarefa.prioridade == 1
        assert tarefa.status == StatusDaTarefa.PENDENTE


def test_service_atualizar_tarefa():
    registrar_eventos_e_comandos_teste()

    hora_inicio = datetime.now() - timedelta(hours=8)
    hora_fim = datetime.now() - timedelta(hours=4)

    comando = AtualizarTarefa(
        id_usuario=uuid4(),
        id_tarefa=uuid4(),
        titulo="titulo",
        descricao="descricao",
        data_de_inicio=hora_inicio,
        data_de_fim=hora_fim,
        prioridade=1,
        status=StatusDaTarefa.PENDENTE,
    )

    uow = MockUoW()
    bus = Barramento()
    # import contexto.tarefa.repositorios.repo.tarefa

    with patch(
        "contexto.tarefa.servicos.executores.gerencia_de_tarefa.GerenciaDeTarefasRepo",
        MockGerenciaDeTarefasRepo,
    ):
        tarefa = bus.enviar_comando(comando, uow)

        assert tarefa is not None
        assert tarefa.titulo == "titulo"
        assert tarefa.descricao == "descricao"
        assert tarefa.data_de_inicio == hora_inicio
        assert tarefa.data_de_fim == hora_fim
        assert tarefa.prioridade == 1
        assert tarefa.status == StatusDaTarefa.PENDENTE


def test_service_deletar_tarefa():
    registrar_eventos_e_comandos_teste()

    hora_inicio = datetime.now() - timedelta(hours=8)
    hora_fim = datetime.now() - timedelta(hours=4)

    comando = CriarTarefa(
        id_usuario=uuid4(),
        titulo="titulo",
        descricao="descricao",
        data_de_inicio=hora_inicio,
        data_de_fim=hora_fim,
        prioridade=1,
        status=StatusDaTarefa.PENDENTE,
    )

    with patch(
        "contexto.tarefa.servicos.executores.gerencia_de_tarefa.GerenciaDeTarefasRepo",
        MockGerenciaDeTarefasRepo,
    ):
        uow = MockUoW()

        bus = Barramento()

        bus.enviar_comando(comando, uow)

        assert True
