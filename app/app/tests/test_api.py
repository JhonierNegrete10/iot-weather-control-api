from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from app.db.configDatabase import engine
from main import app  
from weather.models import WeatherAPIResponse

client = TestClient(app)


# Test cases
def test_get_weather_data_raw_from_api():
    location_params = {"city_name": "London"}
    response = client.post("/api/data/raw", json=location_params)
    assert response.status_code == 200
    assert "weather" in response.json()
    assert "name" in response.json()



def test_get_weather_data_from_api():
    response = client.get("/api/data/")
    assert response.status_code == 200
    assert "city_name" in response.json()


def test_store_weather_data():
    # Create a mock WeatherAPIResponse object
    weather_data = WeatherAPIResponse(
        city_name="Test City",
        city_id="123",
        temperature=20.0,
        pressure=1013,
        description="clear sky",
        icon="01d",
        lon=0.0,
        lat=0.0,
        weather_api_id="800",
        humidity=50,
        wind_speed=1.5,
        wind_deg=90,
        country="TC",
    )
    response = client.post("/api/data", json=weather_data.model_dump())
    assert response.status_code == 200
    assert response.json()["city_name"] == "Test City"


def test_get_weather_data_by_id():
    # Assuming we have a record with ID 1 in the test database
    response = client.get("/api/data/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_start_background_task():
    response = client.post("/api/start")
    assert response.status_code == 200
    assert response.json()["message"] == "Background task started"


def test_stop_background_task():
    response = client.post("/api/stop")
    assert response.status_code == 200
    assert response.json()["message"] == "Background task stopped"


# Run the tests
if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)  # Create tables for the test database
    try:
        # Run the tests
        test_get_weather_data_raw_from_api()
        test_get_weather_data_from_api()
        test_store_weather_data()
        test_get_weather_data_by_id()
        test_start_background_task()
        test_stop_background_task()
    finally:
        # Drop the test database tables after the tests are done
        SQLModel.metadata.drop_all(engine)
