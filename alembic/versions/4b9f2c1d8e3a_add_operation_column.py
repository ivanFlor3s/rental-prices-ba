"""add operation column

Revision ID: 4b9f2c1d8e3a
Revises: e67ac4de4df3
Create Date: 2026-09-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b9f2c1d8e3a'
down_revision: Union[str, Sequence[str], None] = 'e67ac4de4df3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'departments',
        sa.Column('operation', sa.String(length=20), server_default='rent', nullable=False)
    )
    op.create_check_constraint(
        'ck_departments_operation',
        'departments',
        "operation IN ('rent', 'sale')"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('ck_departments_operation', 'departments', type_='check')
    op.drop_column('departments', 'operation')
