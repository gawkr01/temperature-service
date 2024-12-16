from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# These schemas define the request and response formats.
class TemperatureCreate(BaseModel):
    building_id: str = Field(..., example="BuildingA")
    room_id: str = Field(..., example="Room101")
    temperature: float = Field(..., example=22.5)

class TemperatureResponse(BaseModel):
    building_id: str
    room_id: str
    timestamp: datetime
    temperature: float

class AverageTemperatureResponse(BaseModel):
    building_id: str
    room_id: str
    average_temperature: float
    start_time: datetime
    end_time: datetime
