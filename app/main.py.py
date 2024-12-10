from fastapi import FastAPI, Depends, HTTPException
from . import schemas, crud, models
from .database import Base, engine, get_db
from sqlalchemy.orm import Session

# I have set up a FastAPI app to handle the endpoints.
app = FastAPI(
    title="Temperature Service",
    description="This API lets me store and retrieve temperature data.",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

@app.post("/temperatures", response_model=schemas.TemperatureResponse)
def create_temperature_record(data: schemas.TemperatureCreate, db: Session = Depends(get_db)):
    # Create a new temperature record
    record = crud.create_temperature_record(db, data)
    return {
        "building_id": record.building_id,
        "room_id": record.room_id,
        "timestamp": record.timestamp,
        "temperature": record.temperature
    }

@app.get("/temperatures/average", response_model=schemas.AverageTemperatureResponse)
def get_15m_average(building_id: str, room_id: str, db: Session = Depends(get_db)):
    # Get the 15-minute average temperature
    avg_temp, start_time, end_time = crud.get_average_temperature(db, building_id, room_id)
    if avg_temp is None:
        # If no records found, return a 404
        raise HTTPException(status_code=404, detail="No temperature records found in the last 15 minutes.")
    return {
        "building_id": building_id,
        "room_id": room_id,
        "average_temperature": avg_temp,
        "start_time": start_time,
        "end_time": end_time
    }
