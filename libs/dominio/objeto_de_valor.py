from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class ObjetoDeValor(ABC):
    arbitrary_types_allowed = True
