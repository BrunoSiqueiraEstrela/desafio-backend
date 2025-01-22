from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario
from contexto.usuario.dominio.objeto_de_valor.conta_de_usuario import NivelDeAcesso


# primeiro teste
def test_criacao_de_usuario():
    usuario = Usuario.criar(
        nome="João",
        email="email@email.com",
        senha="123456",
        nivel_de_acesso=NivelDeAcesso.USUARIO,
    )

    assert usuario is not None
    assert usuario.nome == "João"
    assert usuario.email == "email@email.com"
    assert usuario.verificar_senha("123456") is True
    assert usuario.nivel_de_acesso == NivelDeAcesso.USUARIO


def test_atualizacao_de_usuario():
    usuario = Usuario.criar(
        nome="João",
        email="email@email",
        senha="123456",
        nivel_de_acesso=NivelDeAcesso.USUARIO,
    )

    usuario.atualizar(
        nome="João da Silva",
        email="novo@email",
        senha="654321",
        nivel_de_acesso=NivelDeAcesso.ADMINISTRADOR,
    )

    assert usuario.nome == "João da Silva"
    assert usuario.email == "novo@email"
    assert usuario.senha == "654321"
    assert usuario.nivel_de_acesso == NivelDeAcesso.ADMINISTRADOR


def test_autualizacao_de_usuario_com_nivel_de_acesso_invalido():
    ...
    # with pytest.raises(ValidationError):


def test_deletar_usuario():
    usuario = Usuario.criar(
        nome="João",
        email="email@email",
        senha="123456",
        nivel_de_acesso=NivelDeAcesso.USUARIO,
    )

    usuario.deletar()

    assert usuario.ativo is False
    assert usuario.deletado_em is not None
