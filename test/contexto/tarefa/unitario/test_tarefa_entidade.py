from datetime import datetime, timedelta
from uuid import uuid4
from freezegun import freeze_time

from contexto.tarefa.dominio.entidades.gerencia_de_tarefa import Tarefa


def test_criar_tarefa():
    tarefa: Tarefa = Tarefa.criar(
        id_usuario=uuid4(),
        titulo="titulo",
        descricao="descricao",
        data_de_inicio="2021-09-01T00:00:00",
        data_de_fim="2021-09-02T00:00:00",
        prioridade=1,
        status="PENDENTE",
    )

    assert tarefa is not None
    assert tarefa.titulo == "titulo"
    assert tarefa.descricao == "descricao"
    assert tarefa.data_de_inicio == "2021-09-01T00:00:00"
    assert tarefa.data_de_fim == "2021-09-02T00:00:00"
    assert tarefa.prioridade == 1
    assert tarefa.status == "PENDENTE"


def test_atualizar_toda_tarefa():
    tarefa: Tarefa = Tarefa.criar(
        id_usuario=uuid4(),
        titulo="titulo",
        descricao="descricao",
        data_de_inicio="2021-09-01T00:00:00",
        data_de_fim="2021-09-02T00:00:00",
        prioridade=1,
        status="PENDENTE",
    )

    tarefa.atualizar(
        titulo="titulo atualizado",
        descricao="descricao atualizada",
        data_de_inicio="2021-09-01T00:00:00",
        data_de_fim="2021-09-02T00:00:00",
        prioridade=2,
        status="CONCLUIDA",
    )

    assert tarefa is not None
    assert tarefa.titulo == "titulo atualizado"
    assert tarefa.descricao == "descricao atualizada"
    assert tarefa.data_de_inicio == "2021-09-01T00:00:00"
    assert tarefa.data_de_fim == "2021-09-02T00:00:00"
    assert tarefa.prioridade == 2


def test_atualizar_um_campo_por_vez():
    tarefa: Tarefa = Tarefa.criar(
        id_usuario=uuid4(),
        titulo="titulo",
        descricao="descricao",
        data_de_inicio="2021-09-01T00:00:00",
        data_de_fim="2021-09-02T00:00:00",
        prioridade=1,
        status="PENDENTE",
    )

    tarefa.atualizar(
        titulo="titulo atualizado",
    )
    assert tarefa.titulo == "titulo atualizado"
    tarefa.atualizar(
        descricao="descricao atualizada",
    )
    assert tarefa.descricao == "descricao atualizada"
    tarefa.atualizar(
        data_de_inicio="2021-09-01T00:00:00",
    )

    assert tarefa.data_de_inicio == "2021-09-01T00:00:00"
    tarefa.atualizar(
        data_de_fim="2021-09-02T00:00:00",
    )
    assert tarefa.data_de_fim == "2021-09-02T00:00:00"
    tarefa.atualizar(
        prioridade=2,
    )
    assert tarefa.prioridade == 2
    tarefa.atualizar(
        status="CONCLUIDA",
    )
    assert tarefa.status == "CONCLUIDA"
    assert tarefa is not None


def test_tarefa_esta_atrasada():
    hora_inicio = datetime.now() - timedelta(hours=8)
    hora_fim = datetime.now() - timedelta(hours=4)
    hora_agora = datetime.now()

    with freeze_time(hora_agora):
        tarefa: Tarefa = Tarefa.criar(
            id_usuario=uuid4(),
            titulo="titulo",
            descricao="descricao",
            data_de_inicio=hora_inicio,
            data_de_fim=hora_fim,
            prioridade=1,
            status="PENDENTE",
        )
        assert tarefa.esta_atrasada()


def test_tarefa_nao_esta_atrasada():
    hora_inicio = datetime.now() - timedelta(hours=8)
    hora_fim = datetime.now() - timedelta(hours=4)
    hora_agora = datetime.now() - timedelta(hours=6)

    with freeze_time(hora_agora):
        tarefa: Tarefa = Tarefa.criar(
            id_usuario=uuid4(),
            titulo="titulo",
            descricao="descricao",
            data_de_inicio=hora_inicio,
            data_de_fim=hora_fim,
            prioridade=1,
            status="PENDENTE",
        )
        assert not tarefa.esta_atrasada()


# --Servico--#


# def test_servico_criar_tarefa():
#     comando = CriarTarefa(
#         id_usuario=uuid4(),
#         titulo="titulo",
#         descricao="descricao",
#         data_de_inicio=datetime.now(),
#         data_de_fim=datetime.now(),
#         prioridade=1,
#         status=StatusDaTarefa.PENDENTE,
#     )

#     uow = MagicMock(spec=UnidadeDeTrabalho)
#     uow.session = MagicMock()

#     repositorio_mock = MagicMock(spec=RepositorioDeTarefas)
#     repositorio_patch = patch(
#         "contexto.tarefa.repositorios.repo.tarefa.RepositorioDeTarefas",
#         return_value=repositorio_mock,
#     )
#     repositorio_patch.start()

#     # Executar a função de criação
#     tarefa = criar_tarefa(comando, uow)
#     # Verificar se os métodos corretos foram chamados
#     repositorio_mock.salvar.assert_called_once()
#     uow.commit.assert_called_once()
#     assert tarefa.titulo == comando.titulo
#     assert tarefa.descricao == comando.descricao
#     repositorio_patch.stop()


# def test_servico_atualizar_tarefa():
#     tarefa = Tarefa.criar(
#         id_usuario=uuid4(),
#         titulo="titulo",
#         descricao="descricao",
#         data_de_inicio=datetime.now(),
#         data_de_fim=datetime.now(),
#         prioridade=1,
#         status=StatusDaTarefa.PENDENTE,
#     )

#     comando = AtualizarTarefa(
#         id_tarefa=tarefa.id,
#         id_usuario=tarefa.id_usuario,
#         titulo="titulo atualizado",
#         descricao="descricao atualizada",
#         data_de_inicio=datetime.now(),
#         data_de_fim=datetime.now(),
#         prioridade=2,
#         status=StatusDaTarefa.CONCLUIDA,
#     )

#     uow = MockUow()
#     mock_repositorio = MagicMock()
#     mock_repositorio.buscar_por_id_de_usuario_e_id_de_tarefa.return_value = tarefa
#     mock_repositorio.atualizar = MagicMock()

#     def mock_repositorio_factory(session):
#         return mock_repositorio

#     global RepositorioDeTarefas
#     RepositorioDeTarefas = mock_repositorio_factory

#     # Executar a função de atualização
#     tarefa_atualizada = atualizar_tarefa(comando, uow)

#     # Verificar se os métodos corretos foram chamados
#     mock_repositorio.atualizar.assert_called_once_with(tarefa_atualizada)
#     assert uow._committed is True
#     assert tarefa_atualizada.titulo == comando.titulo
#     assert tarefa_atualizada.descricao == comando.descricao
#     assert tarefa_atualizada.prioridade == comando.prioridade
#     assert tarefa_atualizada.status == comando.status


# def test_servico_deletar_tarefa():
#     tarefa = Tarefa.criar(
#         id_usuario=uuid4(),
#         titulo="titulo",
#         descricao="descricao",
#         data_de_inicio=datetime.now(),
#         data_de_fim=datetime.now(),
#         prioridade=1,
#         status=StatusDaTarefa.PENDENTE,
#     )

#     comando = DeletarTarefa(
#         id_tarefa=tarefa.id,
#         id_usuario=tarefa.id_usuario,
#     )

#     uow = MockUow()
#     mock_repositorio = MagicMock()
#     mock_repositorio.buscar_por_id_de_usuario_e_id_de_tarefa.return_value = tarefa
#     mock_repositorio.remover = MagicMock()

#     def mock_repositorio_factory(session):
#         return mock_repositorio

#     global RepositorioDeTarefas
#     RepositorioDeTarefas = mock_repositorio_factory

#     # Executar a função de deleção
#     deletar_tarefa(comando, uow)

#     # Verificar se os métodos corretos foram chamados
#     mock_repositorio.remover.assert_called_once_with(comando.id_tarefa)
#     assert uow._committed is True


# def test_servico_atualizar_tarefa_nao_encontrada():
#     comando = AtualizarTarefa(
#         id_tarefa=uuid4(),
#         id_usuario=uuid4(),
#         titulo="titulo atualizado",
#         descricao="descricao atualizada",
#         data_de_inicio=datetime.now(),
#         data_de_fim=datetime.now(),
#         prioridade=2,
#         status=StatusDaTarefa.CONCLUIDA,
#     )

#     uow = MockUow()
#     mock_repositorio = MagicMock()
#     mock_repositorio.buscar_por_id_de_usuario_e_id_de_tarefa.return_value = None

#     def mock_repositorio_factory(session):
#         return mock_repositorio

#     global RepositorioDeTarefas
#     RepositorioDeTarefas = mock_repositorio_factory

#     # Executar a função de atualização e verificar se a exceção é levantada
#     try:
#         atualizar_tarefa(comando, uow)
#     except ErroAoAtualizarTarefa as e:
#         assert str(e) == "Tarefa não encontrada"
#         assert e.status_code == 404


# def test_servico_deletar_tarefa_nao_encontrada():
#     comando = DeletarTarefa(
#         id_tarefa=uuid4(),
#         id_usuario=uuid4(),
#     )

#     uow = MockUow()
#     mock_repositorio = MagicMock()
#     mock_repositorio.buscar_por_id_de_usuario_e_id_de_tarefa.return_value = None

#     def mock_repositorio_factory(session):
#         return mock_repositorio

#     global RepositorioDeTarefas
#     RepositorioDeTarefas = mock_repositorio_factory

#     # Executar a função de deleção e verificar se a exceção é levantada
#     try:
#         deletar_tarefa(comando, uow)
#     except ErroAoDeletarTarefa as e:
#         assert str(e) == "Tarefa não encontrada"
#         assert e.status_code == 404


# class TestCriarTarefa(TestCase):

#     def setUp(self):
#         # Carrega a tabela de usuario
#         from contexto.usuario.repositorios.orm.tarefa import tabela_usuario

#         self.comando = CriarTarefa(
#             id_usuario=uuid4(),
#             titulo="titulo",
#             descricao="descricao",
#             data_de_inicio=datetime.now(),
#             data_de_fim=datetime.now(),
#             prioridade=1,
#             status=StatusDaTarefa.PENDENTE,
#         )
#         self.uow = MagicMock(spec=UnidadeDeTrabalho)  # Simula a unidade de trabalho

#     @patch("contexto.tarefa.repositorios.repo.tarefa.RepositorioDeTarefas.salvar")
#     def test_criar_tarefa_valida(self, mock_salvar):

#         # Arrange
#         mock_salvar.return_value = None

#         # Act
#         tarefa = criar_tarefa(self.comando, self.uow)

#         # Assert
#         self.assertIsInstance(tarefa, Tarefa)
#         mock_salvar.assert_called_once_with(tarefa)
#         self.uow.commit.assert_called_once()
#         self.assertEqual(tarefa.titulo, self.comando.titulo)
#         self.assertEqual(tarefa.descricao, self.comando.descricao)


# class TestAtualizarTarefa(TestCase):
#     from contexto.tarefa.repositorios.orm.tarefa import tabela_tarefa

#     def setUp(self):

#         self.tarefa = Tarefa.criar(
#             id_usuario=uuid4(),
#             titulo="titulo",
#             descricao="descricao",
#             data_de_inicio=datetime.now(),
#             data_de_fim=datetime.now(),
#             prioridade=1,
#             status=StatusDaTarefa.PENDENTE,
#         )

#         self.comando = AtualizarTarefa(
#             id_tarefa=self.tarefa.id,
#             id_usuario=self.tarefa.id_usuario,
#             titulo="titulo atualizado",
#             descricao="descricao atualizada",
#             data_de_inicio=datetime.now(),
#             data_de_fim=datetime.now(),
#             prioridade=2,
#             status=StatusDaTarefa.CONCLUIDA,
#         )

#         self.uow = MagicMock(spec=UnidadeDeTrabalho)
#         self.mock_repositorio = MagicMock(spec=RepositorioTarefas)

#         # self.mock_repositorio.atualizar = MagicMock()

#     @patch("contexto.tarefa.repositorios.repo.tarefa.RepositorioDeTarefas.atualizar")
#     def test_atualizar_tarefa_valida(self, mock_atualizar):

#         self.mock_repositorio.buscar_por_id_de_usuario_e_id_de_tarefa.return_value = (
#             self.tarefa
#         )

#         # Act
#         tarefa_atualizada: Tarefa | None = atualizar_tarefa(self.comando, self.uow)

#         # Assert
#         mock_atualizar.assert_called_once_with(self.tarefa)
#         self.assertTrue(self.uow.commit)
#         self.assertEqual(tarefa_atualizada.titulo, self.comando.titulo)
#         self.assertEqual(tarefa_atualizada.descricao, self.comando.descricao)
#         self.assertEqual(tarefa_atualizada.prioridade, self.comando.prioridade)
#         self.assertEqual(tarefa_atualizada.status, self.comando.status)

#     def test_atualizar_tarefa_nao_encontrada(self):
#         # Arrange
#         self.mock_repositorio.buscar_por_id_de_usuario_e_id_de_tarefa.return_value = (
#             None
#         )

#         # Act & Assert
#         with self.assertRaises(ErroAoAtualizarTarefa) as context:
#             atualizar_tarefa(self.comando, self.uow)

#         self.assertEqual(str(context.exception), "Tarefa não encontrada")
#         self.assertEqual(context.exception.status_code, 404)

#     def test_atualizar_tarefa_erro_ao_atualizar(self):
#         # Arrange
#         self.mock_repositorio.atualizar.side_effect = Exception("Erro ao atualizar")

#         # Act & Assert
#         with self.assertRaises(ErroAoAtualizarTarefa) as context:
#             atualizar_tarefa(self.comando, self.uow)

#         self.assertTrue(
#             "Erro ao atualizar a tarefa: Erro ao atualizar" in str(context.exception)
#         )
#         self.assertEqual(context.exception.status_code, 500)


# class TestDeletarTarefa(TestCase): ...
