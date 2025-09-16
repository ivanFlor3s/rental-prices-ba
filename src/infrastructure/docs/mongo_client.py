from pymongo import MongoClient
import os
# Conexión al servidor (puede ser localhost o un cluster de Mongo Atlas)

string_connection = "mongodb://{user}:{password}@localhost:{port}/".format(
    user=os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin"),
    password=os.getenv("MONGO_INITDB_ROOT_PASSWORD", "admin1234"),
    port=os.getenv("MONGODB_PORT", "27019")
)


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(string_connection)
        self.db = self.client[os.getenv("MONGO_INITDB_DATABASE", "rental_prices")]
        

    def insert_report(self, report):
        collection = self.db['reports']
        result = collection.insert_one(report)
        print(f"Documento insertado con id: {result.inserted_id}")
