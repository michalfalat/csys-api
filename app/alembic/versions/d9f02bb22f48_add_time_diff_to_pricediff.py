"""Add Time Diff to priceDiff

Revision ID: d9f02bb22f48
Revises: 32b84cd02f23
Create Date: 2024-03-27 13:07:30.755443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9f02bb22f48'
down_revision: Union[str, None] = '32b84cd02f23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('price_diffs', sa.Column('time_diff', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('price_diffs', 'time_diff')
    # ### end Alembic commands ###
