from abc import ABC

from pytest import Session


class Repositorio(ABC):
    sql_session: Session

    def __init__(self, sql_session: Session):
        self.sql_session = sql_session
