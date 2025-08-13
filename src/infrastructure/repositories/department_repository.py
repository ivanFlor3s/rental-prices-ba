from sqlalchemy.orm import Session

from infrastructure.db.models import DepartmentModel

class DepartmentRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(DepartmentModel).all()

    def create(self, department: DepartmentModel):
        self.session.add(department)
        self.session.commit()
        self.session.refresh(department)
        return department