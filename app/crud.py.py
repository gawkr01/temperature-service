from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, schemas

# Functions for creating a record and getting the average temperature.
def create_temperature_record(db: Session, data: schemas.TemperatureCreate):
    record = models.TemperatureRecord(
        building_id=data.building_id,
        room_id=data.room_id,
        temperature=data.temperature
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_average_temperature(db: Session, building_id: str, room_id: str):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=15)
    records = db.query(models.TemperatureRecord).filter(
        models.TemperatureRecord.building_id == building_id,
        models.TemperatureRecord.room_id == room_id,
        models.TemperatureRecord.timestamp >= start_time,
        models.TemperatureRecord.timestamp <= end_time
    ).all()

    if not records:
        return None, start_time, end_time

    avg_temp = sum(r.temperature for r in records) / len(records)
    return avg_temp, start_time, end_time
