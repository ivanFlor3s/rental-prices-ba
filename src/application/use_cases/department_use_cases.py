from src.domain.entities.dapartment import Department
from sqlalchemy.orm import Session
from src.utils.mappers import map_department_to_model
from src.infrastructure.db.models import DepartmentModel
from src.domain import enum
from datetime import datetime, timezone

def create_department_from_scrapping(source:str, neighborhood_id: int, department: Department, session: Session):
    existing = session.query(DepartmentModel).filter(DepartmentModel.url == department.url).first()
    if existing:
        existing.title = department.title
        existing.price = department.price
        existing.currency_price = enum.Currency.USD if department.is_usd else enum.Currency.ARS
        existing.expenses = department.expenses
        if department.details:
            existing.rooms = department.details.ambientes
            existing.bedrooms = department.details.bedrooms
            existing.bathrooms = department.details.bathrooms
            existing.surface_total = department.details.area
            existing.garages = department.details.garages
        existing.scraped_at = datetime.now(timezone.utc)
        existing.is_active = True
        session.commit()
        session.refresh(existing)
        return existing
    else:
        new_department = map_department_to_model(department, source=source, neighborhood_id=neighborhood_id)
        session.add(new_department)
        session.commit()
        session.refresh(new_department)
        return new_department
