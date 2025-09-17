
from src.infrastructure.docs.mongo_client import MongoDBClient
from src.infrastructure.repositories.neighborhood_repository import NeighborhoodRepository
from src.infrastructure.db.session import engine
from sqlalchemy.orm import Session

def publish_neighborhoods():
    session = Session(bind=engine)
    repository = NeighborhoodRepository(session)
    neighborhoods = [n.to_dict() for n in repository.get_all()]
    MongoDBClient().insert_neighborhoods( {"neighborhoods": neighborhoods, "location": "CABA"})