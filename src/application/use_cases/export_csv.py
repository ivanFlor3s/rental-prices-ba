import csv
from pathlib import Path

from sqlalchemy.orm import Session

from src.infrastructure.db.models import DepartmentModel, NeighborhoodModel
from src.infrastructure.db.session import engine
from src.infrastructure.logging.config import logger

FIELDNAMES = [
    "id",
    "source",
    "url",
    "title",
    "neighborhood",
    "property_type",
    "operation",
    "rooms",
    "bedrooms",
    "bathrooms",
    "surface_total",
    "garages",
    "price",
    "currency_price",
    "expenses",
    "currency_expenses",
    "is_active",
    "scraped_at",
]


def export_departments_to_csv(file_path: str = "departments.csv") -> str:
    """Exporta los departamentos persistidos a un archivo CSV."""
    session = Session(engine)
    try:
        rows = (
            session.query(DepartmentModel, NeighborhoodModel.name)
            .join(NeighborhoodModel, DepartmentModel.neighborhood_id == NeighborhoodModel.id)
            .all()
        )

        output = Path(file_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDNAMES)
            for dept, neighborhood_name in rows:
                writer.writerow(
                    [
                        dept.id,
                        dept.source,
                        dept.url,
                        dept.title,
                        neighborhood_name,
                        dept.property_type,
                        dept.operation,
                        dept.rooms,
                        dept.bedrooms,
                        dept.bathrooms,
                        dept.surface_total,
                        dept.garages,
                        dept.price,
                        dept.currency_price,
                        dept.expenses,
                        dept.currency_expenses,
                        dept.is_active,
                        dept.scraped_at,
                    ]
                )

        logger.info(f"Se exportaron {len(rows)} departamentos a {output}")
        return str(output)
    finally:
        session.close()
