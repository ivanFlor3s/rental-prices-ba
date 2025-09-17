from dataclasses import dataclass

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
class MeanStackChart:
    metadata: Metadata
    labels: ChartLabels
    filters: ChartFilters
    data: list[MeanData]
    
    def to_dict(self):
        return {
            "metadata": self.metadata.to_dict(),
            "labels": self.labels.to_dict(),
            "filters": self.filters.to_dict(),
            "data": [data.to_dict() for data in self.data]
        }

