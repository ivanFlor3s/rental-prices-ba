from dataclasses import dataclass
from typing import Generic, List, TypeVar, Protocol

class ChartDataProtocol(Protocol):
    def to_dict(self) -> dict:
        ...
        
T = TypeVar('T', bound=ChartDataProtocol)

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
class SurfacePriceData:
    neighborhoodId: int
    neighborhoodName: str
    averagePriceMM: int

    def to_dict(self):
        return {
            "neighborhoodId": self.neighborhoodId,
            "neighborhoodName": self.neighborhoodName,
            "averagePriceMM": self.averagePriceMM,
        }
        

@dataclass
class Metadata:
    generatedAt: str
    totalDepartments: int
    totalNeighborhoods: int
    analysisType: str
    def to_dict(self):
        return {
            "generatedAt": self.generatedAt,
            "totalDepartments": self.totalDepartments,
            "totalNeighborhoods": self.totalNeighborhoods,
            "analysisType": self.analysisType,
        }

@dataclass
class Chart(Generic[T]):
    metadata: Metadata
    labels: ChartLabels
    filters: ChartFilters
    data: List[T]
    
    def to_dict(self):
        return {
            "metadata": self.metadata.to_dict(),
            "labels": self.labels.to_dict(),
            "filters": self.filters.to_dict(),
            "data": [item.to_dict() for item in self.data]
        }

# Type aliases para mayor claridad
MeanChart = Chart[MeanData]
SurfaceChart = Chart[SurfacePriceData]

