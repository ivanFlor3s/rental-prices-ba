from sqlalchemy.orm import Session

from infrastructure.db.models import DepartmentModel

class DepartmentRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(DepartmentModel).all()
    
    def get_by_name(self, name: str):
        """Retrieve a department by its name. It compares the name in a case-insensitive manner."""
        return self.session.query(DepartmentModel).filter(DepartmentModel.name.ilike(name)).first()

    def create(self, department: DepartmentModel):
        self.session.add(department)
        self.session.commit()
        self.session.refresh(department)
        return department