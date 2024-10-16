"""added subscriber table

Revision ID: 7c407cf18869
Revises: 
Create Date: 2024-10-13 15:08:37.205692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c407cf18869'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscribers',
    sa.Column('telegram_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('telegram_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscribers')
    # ### end Alembic commands ###