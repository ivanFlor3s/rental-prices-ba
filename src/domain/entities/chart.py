from dataclasses import dataclass
from typing import Generic, List, TypeVar, Protocol
from typing import Literal

class ChartDataProtocol(Protocol):
    def to_dict(self) -> dict:
        ...
        
T = TypeVar('T', bound=ChartDataProtocol)

PropertyType = Literal["Venta", "Alquiler"]
OperationType = Literal["Departamento", "Casa"]
ProviderType = Literal["ZonaProp"]

@dataclass
class ChartLabels:
    x: str
    y: str
    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y
        }

@dataclass
class ChartFilters:
    rooms: int
    def to_dict(self):
        return {
            "rooms": self.rooms
        }
    

@dataclass
class MeanData:
    neighborhoodId: int
    neighborhoodName: str
    averageExpense: int
    averagePrice: int
    sample: int

    def to_dict(self):
        return {
            "neighborhoodId": self.neighborhoodId,
            "neighborhoodName": self.neighborhoodName,
            "averageExpense": self.averageExpense,
            "averagePrice": self.averagePrice,
            "sample": self.sample
        }
    
    
@dataclass 
class MeanChartData: 
    filters: ChartFilters
    data: List[MeanData]
    def to_dict(self):
        return {
            "filters": self.filters.to_dict(),
            "data": [d.to_dict() for d in self.data]
        }
    
@dataclass 
class SurfacePriceData:
    neighborhoodId: int
    neighborhoodName: str
    averagePriceMM: int
    medianPriceMM: int

    def to_dict(self):
        return {
            "neighborhoodId": self.neighborhoodId,
            "neighborhoodName": self.neighborhoodName,
            "averagePriceMM": self.averagePriceMM,
            "medianPriceMM": self.medianPriceMM
        }
        

@dataclass
class Metadata:
    generatedAt: str
    location: str
    propertyType: PropertyType
    operationType: OperationType
    provider: ProviderType
    def to_dict(self):
        return {
            "generatedAt": self.generatedAt,
            "location": self.location,
            "propertyType": self.propertyType,
            "operationType": self.operationType,
            "provider": self.provider
        }
    
@dataclass
class ChartsData:
    meanData: MeanChartData
    surfacePriceData: List[SurfacePriceData]

    def to_dict(self) -> dict:
        return {
            "mean": [data.to_dict() for data in self.meanData],
            "surface": [data.to_dict() for data in self.surfacePriceData]
        }

@dataclass
class Report():
    metadata: Metadata
    chartsData: ChartsData
    
    def to_dict(self):
        return {
            "metadata": self.metadata.to_dict(),
            "chartsData": self.chartsData.to_dict()
        }



