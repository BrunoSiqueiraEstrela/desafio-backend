"""add_dados_default

Revision ID: 353d82eeb417
Revises: 54036014b612
Create Date: 2025-01-26 19:12:39.018839

"""

from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from contexto.calculo_de_valores.dominio.entidades.carteira import Carteira
from contexto.usuario.dominio.entidades.conta_de_usuario import Usuario


# revision identifiers, used by Alembic.
revision: str = "353d82eeb417"
down_revision: Union[str, None] = "54036014b612"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert two users
    user1_id = uuid4()
    user2_id = uuid4()

    senha1_hash = Usuario.gerar_hash_da_senha(senha="password1")
    senha2_hash = Usuario.gerar_hash_da_senha(senha="password2")

    op.execute(
        f"""
        INSERT INTO "Usuario" (id, nome, email, senha, nivel_de_acesso, ativo, criado_em, atualizado_em)
        VALUES
        ('{user1_id}', 'Usuario UM', 'usuario1@email.com', '{senha1_hash}', 'ADMINISTRADOR', true, '{datetime.now()}', '{datetime.now()}'),
        ('{user2_id}', 'Usuario Dois', 'usuario2@email.com', '{senha2_hash}', 'USUARIO', true, '{datetime.now()}', '{datetime.now()}')
        """
    )

    # Insert wallets for each user
    wallet1_id = uuid4()
    wallet2_id = uuid4()
    op.execute(
        f"""
        INSERT INTO "Carteira" (id, id_usuario, saldo_em_centavos, criado_em, atualizado_em)
        VALUES
        ('{wallet1_id}', '{user1_id}', 10000, '{datetime.now()}', '{datetime.now()}'),
        ('{wallet2_id}', '{user2_id}', 20000, '{datetime.now()}', '{datetime.now()}')
        """
    )

    # Insert transfers for each user
    transfer1_id = uuid4()
    transfer2_id = uuid4()
    transfer3_id = uuid4()
    transfer4_id = uuid4()
    op.execute(
        f"""
        INSERT INTO "Transferencia" (id, id_usuario_origem, id_carteira_origem, id_usuario_destino, id_carteira_destino, valor_transferido_em_centavos, status_da_transferencia, transferido_em, criado_em, atualizado_em)
        VALUES
        ('{transfer1_id}', '{user1_id}', '{wallet1_id}', '{user2_id}', '{wallet2_id}', 5000, 'CONCLUIDO', '2024-01-01 12:00:00', '{datetime.now()}', '{datetime.now()}'),
        ('{transfer2_id}', '{user2_id}', '{wallet2_id}', '{user1_id}', '{wallet1_id}', 3000, 'CONCLUIDO', '2024-01-01 12:00:00', '{datetime.now()}', '{datetime.now()}'),
        ('{transfer3_id}', '{user1_id}', '{wallet1_id}', '{user2_id}', '{wallet2_id}', 7000, 'CONCLUIDO', '2023-01-01 12:00:00', '{datetime.now()}', '{datetime.now()}'),
        ('{transfer4_id}', '{user2_id}', '{wallet2_id}', '{user1_id}', '{wallet1_id}', 4000, 'CONCLUIDO', '2023-01-01 12:00:00', '{datetime.now()}', '{datetime.now()}')
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM \"Transferencia\" WHERE id IN ('{transfer1_id}', '{transfer2_id}', '{transfer3_id}', '{transfer4_id}')"
    )
    op.execute("DELETE FROM \"Carteira\" WHERE id IN ('{wallet1_id}', '{wallet2_id}')")
    op.execute("DELETE FROM \"Usuario\" WHERE id IN ('{user1_id}', '{user2_id}')")
