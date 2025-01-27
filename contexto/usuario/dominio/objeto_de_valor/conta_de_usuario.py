from enum import Enum
from libs.tipos.uuid import ID


class UsuarioID(ID):
    pass


class NivelDeAcesso(Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    USUARIO = "USUARIO"
