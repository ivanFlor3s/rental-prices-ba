from src.application.use_cases.analize_data_use_case import analize_data
from src.domain.entities.mean_stack_chart import ChartFilters, MeanStackChart,ChartLabels
from src.infrastructure.docs.mongo_client import MongoDBClient

def analize_persist_data():  
    client = MongoDBClient()
    max_rooms = 5
    filters = [ChartFilters(rooms=None)] + [ChartFilters(rooms=i) for i in range(1, max_rooms + 1)]
    for filter in filters:
        data = analize_data(filter)
        to_insert = MeanStackChart(
            labels=ChartLabels(x="Amount($)", y="Barrio"),
            filters=filter,
            data= data["data"],
            metadata=data["metadata"],
        )
        client.insert_report(to_insert.to_dict())
