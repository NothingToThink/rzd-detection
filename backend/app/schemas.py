from pydantic import BaseModel
from typing import List, Dict

class Coordinates(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class Rail(BaseModel):
    id: str
    connections: List[str]
    status: str
    coordinates: Coordinates
    is_curve: bool = True

    class Config:
        orm_mode = True
