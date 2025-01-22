from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalhoAbastrato


class MockUoW(UnidadeDeTrabalhoAbastrato):
    def __init__(self):
        self.session = None
        self._committed = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def commit(self):
        self._committed = True

    def rollback(self):
        self._committed = False
