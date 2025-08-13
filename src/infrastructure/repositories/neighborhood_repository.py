
from sqlalchemy.orm import Session

from infrastructure.db.models import NeighborhoodModel


class NeighborhoodRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(NeighborhoodModel).all()

    def create(self, neighborhood: NeighborhoodModel):
        self.session.add(neighborhood)
        self.session.commit()
        self.session.refresh(neighborhood)
        return neighborhood
