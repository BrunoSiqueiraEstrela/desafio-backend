from typing import Final
from sqlalchemy.orm import registry
from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm.session import Session, sessionmaker
from libs.variaveis.gerenciador_de_env import ENVS

REGISTRO_DOS_ORMS: Final = registry()
metadata = MetaData()


def conectar() -> Session:
    engine: Engine = create_engine(
        ENVS.DB_STRING_CONNECTION, isolation_level="AUTOCOMMIT"
    )
    _session = sessionmaker(bind=engine, expire_on_commit=False)

    return _session()
