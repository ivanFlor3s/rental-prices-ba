
from sqlalchemy.orm import Session

from src.infrastructure.db.models import NeighborhoodModel


class NeighborhoodRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(NeighborhoodModel).all()
    
    def get_by_name(self, name: str):
        """Retrieve a neighborhood by its name. It compares the name in a case-insensitive manner."""
        return self.session.query(NeighborhoodModel).filter(NeighborhoodModel.name.ilike(name)).first()

    def create(self, neighborhood: NeighborhoodModel):
        self.session.add(neighborhood)
        self.session.commit()
        self.session.refresh(neighborhood)
        return neighborhood
