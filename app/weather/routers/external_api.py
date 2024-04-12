import asyncio

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)

# from fastapi.datastructures import QueryParams
from sqlmodel import Session
from weather.services.external_api import fetch_weather_data

from app.db.configDatabase import get_session

from ..crud import weather_api_crud
from ..models import (
    LocationParams,
    WeatherAPIModel,
    WeatherAPIResponse,
    WeatherData,
)

api_routers = APIRouter(prefix="/api", tags=["external-api"])

# Constants
DEFAULT_CITY_NAME = "Medellin"
BACKGROUND_TASK_SLEEP_DURATION = 10  # in seconds


# Helper Functions
async def fetch_and_validate_weather_data(location_params: LocationParams):
    data = fetch_weather_data(**location_params.model_dump())
    if "cod" in data and data["cod"] == "404":
        raise HTTPException(status_code=404, detail="City not found")
    return data


def create_weather_api_response(data) -> WeatherAPIResponse:
    return WeatherAPIResponse(
        city_name=data["name"],
        city_id=str(data["id"]),
        temperature=data["main"]["temp"],
        pressure=data["main"]["pressure"],
        description=data["weather"][0]["description"],
        icon=data["weather"][0]["icon"],
        lon=data["coord"]["lon"],
        lat=data["coord"]["lat"],
        weather_api_id=str(data["weather"][0]["id"]),
        humidity=data["main"]["humidity"],
        wind_speed=data["wind"]["speed"],
        wind_deg=data["wind"]["deg"],
        country=data["sys"]["country"],
    )


# Routes
@api_routers.post("/data/raw", response_model=WeatherData)
async def get_weather_data_raw_from_api(location_params: LocationParams):
    """
    Fetches raw weather data from the OpenWeatherMap API based on location parameters.

    Args:
        location_params (LocationParams): Location parameters for fetching weather data.

    Returns:
        WeatherData: Raw weather data fetched from the API.

    Raises:
        HTTPException: If the city is not found in the API response.
    """

    return await fetch_and_validate_weather_data(location_params)


@api_routers.get("/data/", response_model=WeatherAPIResponse)
async def get_weather_data_from_api():
    """
    Fetches weather data from the OpenWeatherMap API and returns it in a structured format.

    Returns:
        WeatherAPIResponse: Structured weather data response.

    Raises:
        HTTPException: If the city is not found in the API response.
    """
    location_params = LocationParams()
    data = await fetch_and_validate_weather_data(location_params)
    return create_weather_api_response(data)


@api_routers.post("/data", response_model=WeatherAPIModel)
async def store_weather_data(
    weather_api: WeatherAPIResponse, session: Session = Depends(get_session)
):
    """
    Stores weather data in the database.

    Args:
        weather_api (WeatherAPIResponse): Weather data to be stored.
        session (Session): Database session.

    Returns:
        WeatherAPIModel: Weather data stored in the database.
    """
    return weather_api_crud.create(weather_api, session)


@api_routers.get("/data/{id}", response_model=WeatherAPIModel)
async def get_weather_data_by_id(id: int, session: Session = Depends(get_session)):
    """
    Retrieves weather data by ID from the database.

    Args:
        id (int): ID of the weather data to retrieve.
        session (Session): Database session.

    Returns:
        WeatherAPIModel: Weather data retrieved from the database.

    Raises:
        HTTPException: If the weather data with the specified ID is not found.
    """
    weather_api = weather_api_crud.get_by_id(id, session=session)

    if weather_api is None:
        raise HTTPException(status_code=404, detail="City weather data not found")
    return weather_api


# Background Task
background_task = None


async def background_task_function(session):
    """
    Background task function that continuously fetches weather data for a specific city and stores it in the database.

    Args:
        session (Session): Database session.

    Returns:
        None
    """
    while True:
        try:
            data = fetch_weather_data(city_name=DEFAULT_CITY_NAME)
            if "cod" in data and data["cod"] == "404":
                print("Background Task: City not found")
                continue
            weather_api = create_weather_api_response(data)
            weather_api_crud.create(weather_api, session)
            print("Background Task: Data stored")
        except Exception as e:
            print(f"An error occurred Background Task: {e}")
        await asyncio.sleep(BACKGROUND_TASK_SLEEP_DURATION)


@api_routers.post("/start")
async def start_background_task(session: Session = Depends(get_session)):
    """
    Endpoint to start the background task for fetching and storing weather data.

    Args:
        session (Session): Database session.

    Returns:
        dict: Message indicating the status of the background task.
    """
    global background_task
    if background_task is None:
        background_task = asyncio.create_task(background_task_function(session))
        return {"message": "Background task started"}
    else:
        return {"message": "Background task is already running"}


@api_routers.post("/stop")
async def stop_background_task():
    """
    Endpoint to stop the background task for fetching and storing weather data.

    Returns:
        dict: Message indicating the status of the background task.
    """
    global background_task
    if background_task is not None:
        background_task.cancel()
        background_task = None
        return {"message": "Background task stopped"}
    else:
        return {"message": "No background task is currently running"}


# WebSocket endpoint to view data similar to GET /api/data
@api_routers.websocket("/ws/data/")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to view weather data in real-time.

    Args:
        websocket (WebSocket): WebSocket connection.

    Returns:
        None

    Raises:
        WebSocketDisconnect: If the WebSocket connection is disconnected.
    """
    await websocket.accept()
    location_params = LocationParams()
    while True:
        try:
            data = await fetch_and_validate_weather_data(location_params)
            weather_response = create_weather_api_response(data).model_dump()
            await websocket.send_json(weather_response)
            await asyncio.sleep(BACKGROUND_TASK_SLEEP_DURATION)
        except WebSocketDisconnect:
            break
        except HTTPException as e:
            await websocket.send_json({"error": e.detail})
            break
