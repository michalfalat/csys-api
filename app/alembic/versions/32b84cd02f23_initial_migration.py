"""Initial Migration

Revision ID: 32b84cd02f23
Revises: 
Create Date: 2024-03-27 13:04:54.656662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32b84cd02f23'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchanges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price_diff_params',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('exchanges', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('watched_symbols', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('price_diff_threshold', sa.Float(), nullable=True),
    sa.Column('time_diff_threshold', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price_diffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('exchange_1', sa.String(length=50), nullable=True),
    sa.Column('exchange_2', sa.String(length=50), nullable=True),
    sa.Column('exchange_1_date', sa.DateTime(), nullable=True),
    sa.Column('exchange_2_date', sa.DateTime(), nullable=True),
    sa.Column('exchange_1_price', sa.Float(), nullable=True),
    sa.Column('exchange_2_price', sa.Float(), nullable=True),
    sa.Column('exchange_1_symbol', sa.String(length=50), nullable=True),
    sa.Column('exchange_2_symbol', sa.String(length=50), nullable=True),
    sa.Column('price_diff', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('price_diffs')
    op.drop_table('price_diff_params')
    op.drop_table('exchanges')
    # ### end Alembic commands ###
