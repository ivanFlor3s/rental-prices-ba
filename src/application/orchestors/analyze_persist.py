from datetime import datetime
from src.application.use_cases.analize_data_use_case import DataAnalizer
from domain.entities.chart import ChartFilters, Report, MeanChartData, ChartsData, Metadata
from src.infrastructure.docs.mongo_client import MongoDBClient

def analize_persist_data(provider: str, location: str, property_type: str, operation_type: str):  
    client = MongoDBClient()
    max_rooms = 5
    filters = [ChartFilters(rooms=None)] + [ChartFilters(rooms=i) for i in range(1, max_rooms + 1)]
    analizer = DataAnalizer()


    mean =  _get_mean_data(analizer, filters)
    surface = _get_surface_data(analizer)

    report = Report(
        chartsData= ChartsData(
            meanData=mean,
            surfacePriceData=surface
        ),
        metadata= Metadata(
            generatedAt=datetime.now(),
            location=location,
            propertyType=property_type,
            operationType=operation_type,
            provider=provider
        )
    )

    client.insert_report(report.to_dict())




def _get_mean_data(analizer: DataAnalizer, filters: list[ChartFilters]) -> list[MeanChartData]:
    chartData = []
    for filter in filters:
        data = analizer.analize_data_for_mean(filter)
        to_insert = MeanChartData(
            filters=filter,
            data= data
        )
        chartData.append(to_insert)

    return chartData
    

def _get_surface_data(analizer: DataAnalizer):
    data = analizer.analize_data_for_surface_price()
    return data

    

    

