from fastapi.testclient import TestClient
from app.main import app
import time

# I am using the FastAPI test client to test the endpoints.
client = TestClient(app)

def test_create_record():
    response = client.post("/temperatures", json={
        "building_id": "TestBuilding",
        "room_id": "TestRoom",
        "temperature": 25.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["building_id"] == "TestBuilding"
    assert data["room_id"] == "TestRoom"
    assert data["temperature"] == 25.0

def test_get_average_no_data():
    # Checking if average endpoint returns 404 when no records
    response = client.get("/temperatures/average?building_id=NoBuilding&room_id=NoRoom")
    assert response.status_code == 404

def test_get_average_with_data():
    # Create a record first
    client.post("/temperatures", json={
        "building_id": "AvgBuilding",
        "room_id": "AvgRoom",
        "temperature": 20.0
    })
    time.sleep(1)
    response = client.get("/temperatures/average?building_id=AvgBuilding&room_id=AvgRoom")
    assert response.status_code == 200
    data = response.json()
    assert data["average_temperature"] == 20.0
