from src.application.use_cases.analize_data_use_case import DataAnalizer
from src.domain.entities.mean_stack_chart import ChartFilters, Chart,ChartLabels
from src.infrastructure.docs.mongo_client import MongoDBClient

def analize_persist_data():  
    client = MongoDBClient()
    max_rooms = 5
    filters = [ChartFilters(rooms=None)] + [ChartFilters(rooms=i) for i in range(1, max_rooms + 1)]
    analizer = DataAnalizer()
    #_persist_mean_data_to_mongo(analizer, filters, client)
    _persist_surface_data_to_mongo(analizer, client)


def _persist_mean_data_to_mongo(analizer: DataAnalizer, filters: list[ChartFilters], client: MongoDBClient = None):
    for filter in filters:
        data = analizer.analize_data_for_mean(filter)
        to_insert = Chart(
            labels=ChartLabels(x="Amount($)", y="Barrio"),
            filters=filter,
            data= data["data"],
            metadata=data["metadata"],
        )
        client.insert_report(to_insert.to_dict())

def _persist_surface_data_to_mongo(analizer: DataAnalizer, client: MongoDBClient = None):
    data = analizer.analize_data_for_surface_price()
    to_insert = Chart(
        labels=ChartLabels(x="Price per m²($)", y="Barrio"),
        filters=ChartFilters(rooms=None),
        data= data["data"],
        metadata=data["metadata"],
    )
    client.insert_report(to_insert.to_dict())

    

    

