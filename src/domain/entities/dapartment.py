from dataclasses import dataclass
from typing import Optional

@dataclass
class DeptDetails:
    ambientes: int
    bedrooms: int
    bathrooms: int
    area: int
    garages: int


@dataclass
class Department:
    title: str
    url: str
    price: int
    is_usd: bool
    location: str
    expenses: Optional[int] = None
    details: Optional[DeptDetails] = None