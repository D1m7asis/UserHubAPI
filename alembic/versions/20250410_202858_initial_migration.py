"""initial migration

Revision ID: 45cd3bbd4c7e
Revises: 
Create Date: 2025-04-10 20:28:58.343487

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = '45cd3bbd4c7e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger, primary_key=True, index=True, autoincrement=True),
        sa.Column('name', sa.String(255), index=True),
        sa.Column('surname', sa.String(255)),
        sa.Column('password', sa.String(255)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )

    op.create_table(
        'task_results',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('status', sa.String(length=50), index=True),
        sa.Column('result', sa.JSON(), nullable=True),
        sa.Column('error', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
    )


def downgrade() -> None:
    op.drop_table('task_results')
    op.drop_table('users')
