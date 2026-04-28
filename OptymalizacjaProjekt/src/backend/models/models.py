
from pydantic import BaseModel
from typing import List
class Plant(BaseModel):
    name: str
    production_cost: float
    soil_influence: float
    earnings_matrix: List[float]

class FarmConfig(BaseModel):
    field_number: int
    years_number: int
    transport_cost: float
    field_surfaces: List[float]
    distances: List[float]
    start_qualities: List[int]