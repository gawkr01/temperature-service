from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app from your app.main module
import time


# Instantiate the TestClient correctly without passing 'app' as a keyword argument
client = TestClient(app)

def test_post_temperature():
    print("Starting test: test_post_temperature - Testing POST request to /temperatures endpoint with building_id 'BuildingA', room_id 'Room101', and temperature 22.5")
    response = client.post(
        "/temperatures",
        json={"building_id": "BuildingA", "room_id": "Room101", "temperature": 22.5}
    )
    print(f"Response status code: {response.status_code}, Response JSON: {response.json()}")
    assert response.status_code == 200
    assert response.json()["building_id"] == "BuildingA"
    print("Test test_post_temperature passed.")

def test_create_record():
    print("Starting test: test_create_record - Testing POST request to /temperatures to create a new record")
    response = client.post("/temperatures", json={
        "building_id": "TestBuilding",
        "room_id": "TestRoom",
        "temperature": 25.0
    })
    print(f"Response status code: {response.status_code}, Response JSON: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["building_id"] == "TestBuilding"
    assert data["room_id"] == "TestRoom"
    assert data["temperature"] == 25.0
    print("Test test_create_record passed.")

def test_get_average_no_data():
    print("Starting test: test_get_average_no_data - Testing GET request to /temperatures/average with non-existing building and room")
    response = client.get("/temperatures/average?building_id=NoBuilding&room_id=NoRoom")
    print(f"Response status code: {response.status_code}")
    assert response.status_code == 404
    print("Test test_get_average_no_data passed.")

def test_get_average_with_data():
    print("Starting test: test_get_average_with_data - Testing POST request to /temperatures and GET request to /temperatures/average")
    
    # Post temperature data first
    client.post("/temperatures", json={
        "building_id": "AvgBuilding",
        "room_id": "AvgRoom",
        "temperature": 20.0
    })
    print("Posted temperature data for AvgBuilding and AvgRoom with temperature 20.0")
    
    # Sleep to ensure data is processed before fetching average
    time.sleep(1)
    
    # Now get the average temperature
    response = client.get("/temperatures/average?building_id=AvgBuilding&room_id=AvgRoom")
    print(f"Response status code: {response.status_code}, Response JSON: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["average_temperature"] == 20.0
    print("Test test_get_average_with_data passed.")
