from enum import Enum
from libs.tipos.uuid import ID


class UsuarioID(ID): ...


class NivelDeAcesso(Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    USUARIO = "USUARIO"
