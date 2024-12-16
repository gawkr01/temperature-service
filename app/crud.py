from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, schemas

# Function to create a new temperature record in the database.
def create_temperature_record(db: Session, data: schemas.TemperatureCreate):
    """
    Creates a new temperature record in the database.
    
    This function takes temperature data (building ID, room ID, temperature) from the request,
    creates a new record in the database, and returns the created record.
    """
    # Create a new TemperatureRecord object from the input data.
    record = models.TemperatureRecord(
        building_id=data.building_id,
        room_id=data.room_id,
        temperature=data.temperature
    )
    
    # Add the new record to the session and commit the transaction.
    db.add(record)
    db.commit()
    
    # Refresh the record to get the updated details (including the auto-generated timestamp).
    db.refresh(record)
    
    # Return the created record.
    return record

# Function to calculate and return the 15-minute average temperature for a specific building and room.
def get_average_temperature(db: Session, building_id: str, room_id: str):
    """
    Retrieves and calculates the average temperature over the last 15 minutes for a given building and room.
    
    This function queries the database for temperature records within the last 15 minutes 
    for the specified building and room, calculates the average temperature, and returns it along with 
    the start and end times of the 15-minute period.
    """
    # Define the time range for the query (last 15 minutes).
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=15)
    
    # Query the database for records within the specified time range.
    records = db.query(models.TemperatureRecord).filter(
        models.TemperatureRecord.building_id == building_id,
        models.TemperatureRecord.room_id == room_id,
        models.TemperatureRecord.timestamp >= start_time,
        models.TemperatureRecord.timestamp <= end_time
    ).all()

    # If no records are found, return None for average temperature and the time range.
    if not records:
        return None, start_time, end_time

    # Calculate the average temperature from the retrieved records.
    avg_temp = sum(r.temperature for r in records) / len(records)
    
    # Return the average temperature and the time range.
    return avg_temp, start_time, end_time
