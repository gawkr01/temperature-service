from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# These schemas define the request and response formats.

class TemperatureCreate(BaseModel):
    """
    Schema for creating a new temperature record.
    
    This schema defines the structure of the data expected in the request body
    when a new temperature record is created via the POST /temperatures endpoint.
    """
    building_id: str = Field(..., example="BuildingA")
    room_id: str = Field(..., example="Room101")
    temperature: float = Field(..., example=22.5)

class TemperatureResponse(BaseModel):
    """
    Schema for the response when retrieving or creating a temperature record.
    This schema defines the structure of the data returned after creating or retrieving
    a temperature record. It is used as the response model for the POST /temperatures
    and GET /temperatures endpoints.
    """
    building_id: str
    room_id: str
    timestamp: datetime
    temperature: float

class AverageTemperatureResponse(BaseModel):
    """
    Schema for the response when retrieving the average temperature over the last 15 minutes.
    This schema defines the structure of the data returned when calculating the average
    temperature for a specific room in a building over the last 15-minute period.
    It is used as the response model for the GET /temperatures/average endpoint.
    """
    building_id: str
    room_id: str
    average_temperature: float
    start_time: datetime
    end_time: datetime
