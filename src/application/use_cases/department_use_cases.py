from src.domain.entities.dapartment import Department
from sqlalchemy.orm import Session
from src.utils.mappers import map_department_to_model

def create_department_from_scrapping(source:str, neighborhood_id: int, department: Department, session: Session):
    new_department = map_department_to_model(department, source=source, neighborhood_id=neighborhood_id)
    session.add(new_department)
    session.commit()
    session.refresh(new_department)
    return new_department
