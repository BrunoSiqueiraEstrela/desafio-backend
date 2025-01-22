from abc import ABC
from typing import Any, Optional, Self
from dataclasses import dataclass
from sqlalchemy.orm.session import Session
from sqlalchemy import text


@dataclass
class UnidadeDeTrabalhoAbastrato(ABC):
    def __enter__(self) -> Self:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def adicionar(self, obj: Any):
        pass


@dataclass
class UnidadeDeTrabalho(UnidadeDeTrabalhoAbastrato):
    schema: str = "public"
    session: Optional[Session] = None

    def __enter__(self) -> Self:
        from libs.database.config import conectar

        if not self.session:
            self.session = conectar()

        self.session.execute(text(f"SET search_path TO '{self.schema}'"))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def adicionar(self, obj: Any):
        self.session.add(obj)
