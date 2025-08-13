"""Seed neighberhoods

Revision ID: 96e92edbafaf
Revises: 3a94565cc417
Create Date: 2025-08-13 18:10:41.323574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import Session
from src.infrastructure.db.session import engine
from src.infrastructure.db.models import NeighborhoodModel



# revision identifiers, used by Alembic.
revision: str = '96e92edbafaf'
down_revision: Union[str, Sequence[str], None] = '3a94565cc417'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

neighborhoods = [
        "Agronomia",
        "Almagro",
        "Balvanera",
        "Barracas",
        "Belgrano",
        "Boedo",
        "Caballito",
        "Chacarita",
        "Coghlan",
        "Colegiales",
        "Constitucion",
        "Flores",
        "Floresta",
        "La Boca",
        "La Paternal",
        "Liniers",
        "Mataderos",
        "Monte Castro",
        "Monserrat",
        "Nueva Pompeya",
        "Nunez",
        "Palermo",
        "Parque Avellaneda",
        "Parque Chacabuco",
        "Parque Chas",
        "Parque Patricios",
        "Puerto Madero",
        "Recoleta",
        "Retiro",
        "Saavedra",
        "San Cristobal",
        "San Nicolas",
        "San Telmo",
        "Versalles",
        "Villa Crespo",
        "Villa Devoto",
        "Villa General Mitre",
        "Villa Lugano",
        "Villa Luro",
        "Villa Ortuzar",
        "Villa Pueyrredon",
        "Villa Real",
        "Villa Riachuelo",
        "Villa Santa Rita",
        "Villa Soldati",
        "Villa Urquiza",
        "Villa del Parque",
        "Vélez Sarsfield"
]

def upgrade() -> None:
    """Upgrade schema."""
    session = Session(bind=engine)
    try:
        for neighborhood_name in neighborhoods:
            # Check if the neighborhood already exists
            existing_neighborhood = session.query(NeighborhoodModel).filter_by(name=neighborhood_name).first()
            if not existing_neighborhood:
                # Create a new neighborhood entry
                new_neighborhood = NeighborhoodModel(name=neighborhood_name)
                session.add(new_neighborhood)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    pass


def downgrade() -> None:
    """Downgrade schema."""
    session = Session(bind=engine)
    try:
        for neighborhood in neighborhoods:
            # Find the neighborhood by name
            existing_neighborhood = session.query(NeighborhoodModel).filter_by(name=neighborhood).first()
            if existing_neighborhood:
                # Delete the neighborhood entry
                session.delete(existing_neighborhood)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    pass
