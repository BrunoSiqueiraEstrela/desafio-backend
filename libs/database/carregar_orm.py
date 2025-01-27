def carregar_tabelas():
    from contexto.usuario.repositorio.orm.usuario import tabela_usuario  # noqa
    from contexto.calculo_de_valores.repositorio.orm.transferencia import (
        tabela_transferencia,
    )  # noqa
    from contexto.calculo_de_valores.repositorio.orm.carteira import tabela_carteira  # noqa
