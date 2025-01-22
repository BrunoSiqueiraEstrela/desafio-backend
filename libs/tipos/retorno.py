from typing import Generic, TypeVar

from pydantic import BaseModel

T_ID = TypeVar("T_ID")
T = TypeVar("T")


class RetornoApenasId(BaseModel, Generic[T_ID]):
    id: T_ID


class RetornoDeDados(BaseModel, Generic[T]):
    dado: T
