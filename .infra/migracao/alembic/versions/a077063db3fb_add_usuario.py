"""Add Usuario

Revision ID: a077063db3fb
Revises: 
Create Date: 2024-10-01 16:57:02.064667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a077063db3fb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Usuario',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('senha', sa.String(length=100), nullable=False),
    sa.Column('nivel_de_acesso', sa.Enum('ADMINISTRADOR', 'USUARIO', name='niveldeacesso'), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deletado_em', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Usuario_email'), 'Usuario', ['email'], unique=True)
    op.create_index(op.f('ix_Usuario_id'), 'Usuario', ['id'], unique=False)
    op.create_index(op.f('ix_Usuario_nome'), 'Usuario', ['nome'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Usuario_nome'), table_name='Usuario')
    op.drop_index(op.f('ix_Usuario_id'), table_name='Usuario')
    op.drop_index(op.f('ix_Usuario_email'), table_name='Usuario')
    op.drop_table('Usuario')
    # ### end Alembic commands ###
