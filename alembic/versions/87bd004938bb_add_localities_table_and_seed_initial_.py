"""add localities table and seed initial data

Revision ID: 87bd004938bb
Revises: 60d9b900d64f
Create Date: 2025-10-06 16:56:16.898428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87bd004938bb'
down_revision: Union[str, Sequence[str], None] = '60d9b900d64f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


"""seed initial localities"""

from alembic import op
import sqlalchemy as sa

# Revisiones
revision = "87bd004938bb"
down_revision = "60d9b900d64f"  # la migración anterior
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    # Definimos la tabla de destino
    localities_table = sa.table(
        "localities",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )

    # Datos iniciales
    localities = [
        {"name": "CABA"},
        {"name": "GBA Sur"},
        {"name": "GBA Norte"},
        {"name": "GBA Oeste"},
    ]

    # Insertar los registros
    connection.execute(sa.insert(localities_table), localities)


def downgrade():
    connection = op.get_bind()
    connection.execute(sa.text("DELETE FROM localities WHERE name IN ('CABA', 'GBA Sur', 'GBA Norte', 'GBA Oeste')"))
