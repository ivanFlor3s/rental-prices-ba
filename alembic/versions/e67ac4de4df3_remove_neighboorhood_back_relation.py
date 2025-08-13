"""remove neighboorhood back relation

Revision ID: e67ac4de4df3
Revises: 96e92edbafaf
Create Date: 2025-08-13 18:32:00.647821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e67ac4de4df3'
down_revision: Union[str, Sequence[str], None] = '96e92edbafaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
