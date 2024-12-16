from fastapi import FastAPI, Depends, HTTPException
from . import schemas, crud, models
from .database import Base, engine, get_db
from sqlalchemy.orm import Session

# Set up a FastAPI app to handle the endpoints for temperature data storage and retrieval.
app = FastAPI(
    title="Temperature Service",
    description="This API lets me store and retrieve temperature data.",
    version="0.1.0"
)

# Create the database tables defined in the models (if not already created).
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    """
    Root endpoint that provides a welcome message.
    
    This endpoint returns a simple message when accessing the root of the API.
    It serves as a basic check to ensure the service is running.
    """
    return {"message": "Welcome to the Temperature Service API!"}

@app.post("/temperatures", response_model=schemas.TemperatureResponse)
def create_temperature_record(data: schemas.TemperatureCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new temperature record.
    
    This endpoint allows a user to submit a new temperature record for a building and room.
    It takes the temperature data in the request body, creates a new record, and returns 
    the record details including building ID, room ID, timestamp, and temperature.
    """
    # Create a new temperature record by calling the crud function.
    record = crud.create_temperature_record(db, data)
    
    # Return the created record's details.
    return {
        "building_id": record.building_id,
        "room_id": record.room_id,
        "timestamp": record.timestamp,
        "temperature": record.temperature
    }

@app.get("/temperatures/average", response_model=schemas.AverageTemperatureResponse)
def get_15m_average(building_id: str, room_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to get the 15-minute average temperature.
    
    This endpoint calculates and returns the average temperature for a given building and room
    over the last 15 minutes. It also returns the start and end times of the 15-minute period.
    If no records are found, a 404 error is returned.
    """
    # Retrieve the average temperature over the last 15 minutes for the specified building and room.
    avg_temp, start_time, end_time = crud.get_average_temperature(db, building_id, room_id)
    
    # If no records are found, raise an HTTP 404 error.
    if avg_temp is None:
        raise HTTPException(status_code=404, detail="No temperature records found in the last 15 minutes.")
    
    # Return the average temperature data, including start and end times of the 15-minute period.
    return {
        "building_id": building_id,
        "room_id": room_id,
        "average_temperature": avg_temp,
        "start_time": start_time,
        "end_time": end_time
    }
