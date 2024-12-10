from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime

# This model represents a temperature record in the database.
class TemperatureRecord(Base):
    __tablename__ = "temperature_records"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(String, index=True)
    room_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    temperature = Column(Float)
