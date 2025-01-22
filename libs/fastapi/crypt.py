from datetime import datetime, timedelta

import os
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha_hash(senha_em_texto, senha_criptografada):
    return bcrypt.verify(senha_em_texto, senha_criptografada)


def gerar_hash_da_senha(senha: str) -> str:
    return bcrypt.hash(senha)


def criar_token_de_acesso(data: dict, expires_delta: Optional[timedelta] = None):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    para_codificar = data.copy()

    for chave, valor in para_codificar.items():
        if isinstance(valor, UUID):
            para_codificar[chave] = str(valor)

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    para_codificar.update({"exp": expire})
    jwt_codificado = jwt.encode(para_codificar, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_codificado


def decodificar_token(token):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def obter_indentificador(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        dados = decodificar_token(token)
        identificador: str = dados.get("sub")

        if identificador is None:
            raise credentials_exception

    except jwt.JWTError:
        raise credentials_exception
    return identificador
