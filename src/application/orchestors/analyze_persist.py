from src.application.use_cases.analize_data_use_case import analize_data
from src.infrastructure.docs.mongo_client import MongoDBClient

def analize_persist_data():  
    json = analize_data()
    client = MongoDBClient()
    client.insert_report(json)
