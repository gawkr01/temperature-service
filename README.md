# Temperature Service

This is a simple backend service that lets me store and analyze temperature data from different buildings and rooms. I can send temperature readings with a POST request and then get the 15-minute average temperature for a specific building and room with a GET request.

## Why I Chose FastAPI

I have chosen FastAPI for this implementation because:

- It makes it very easy to build RESTful APIs.
- It handles data validation with Pydantic models.
- It is fast and uses modern Python features (async/await).
- It is popular and has good documentation.

## How It Works

- **POST /temperatures**: I can send a JSON body with `building_id`, `room_id`, and `temperature`. The server stores it in the database with a timestamp.
- **GET /temperatures/average?building_id=X&room_id=Y**: I can get the average temperature for the last 15 minutes for that building and room.

I am using a simple SQLite database for this demo. In a real system, I might use PostgreSQL or MySQL.

## How To Run Locally
uvicorn app.main:app --reload

### Requirements

- Python 3.11+
- pip

### Steps

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
2. Run the application:

    uvicorn app.main:app --reload

3. The API will be available at:
    http://127.0.0.1:8000

Examples

    POST Temperature Record:

curl -X POST http://127.0.0.1:8000/temperatures \
     -H "Content-Type: application/json" \
     -d '{"building_id":"BuildingA","room_id":"Room101","temperature":22.5}'

GET 15-minute Average:

    curl "http://127.0.0.1:8000/temperatures/average?building_id=BuildingA&room_id=Room101"

### Running with Docker

1. Build the Docker image:

docker build -t temperature-service:latest .

2. Run the Docker container:

    docker run -p 8000:8000 temperature-service:latest

### Deploying to Kubernetes

I have included some simple Kubernetes manifests in the kubernetes folder. To deploy:

kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

This will create a Deployment and a Service. Adjust as needed for your cluster.

### Testing Strategy

I have used pytest for testing. My tests include:

    Unit tests: Checking if database operations work as expected.
    Integration tests: Using the FastAPI test client to check the endpoints from start to finish.

To run tests:

pytest tests

These tests help ensure that adding a record and retrieving averages works correctly. They also verify that the system returns proper error messages when no data is found.

### CI/CD

My CI/CD idea is:

    On every pull request, run pytest to ensure all tests pass before merging.
    On merge to the main branch, build and push the Docker image, then apply the Kubernetes manifests.
    
HEAD
You can set this up with any CI/CD tool you prefer.


