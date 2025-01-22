from typing import Any
from libs.dominio.comando import Comando
from libs.dominio.evento import Evento
from libs.dominio.unidade_de_trabalho import UnidadeDeTrabalho


class Barramento:
    comandos: set[Comando, callable] = {}
    eventos: set[Evento, list[callable]] = {}

    # SINGLIETON
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwds)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def registrar_comando(self, comando: Comando, callback: callable):
        if not issubclass(comando, Comando):
            raise TypeError("comando deve ser uma classe de Comando")

        self.comandos[comando] = callback

    def registrar_evento(self, evento: Evento, callback: callable):
        if not issubclass(evento, Evento):
            raise TypeError("evento deve ser uma classe de Evento")
        try:
            tem_evento = self.eventos[evento]
            if tem_evento:
                self.eventos[evento].append(callback)
        except KeyError:
            self.eventos[evento] = []
            self.eventos[evento].append(callback)

    def enviar_comando(self, comando: Comando, uow: UnidadeDeTrabalho):
        return self.comandos[comando.__class__](comando, uow)

    def enviar_evento(self, evento: Evento, uow: UnidadeDeTrabalho):
        for callback in self.eventos[evento.__class__]:
            callback(evento, uow)
