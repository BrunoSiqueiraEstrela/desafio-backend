from abc import ABC

from pydantic import BaseModel


class Comando(ABC, BaseModel):
    pass
