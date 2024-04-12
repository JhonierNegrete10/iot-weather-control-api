from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlmodel import Session

from app.db.configDatabase import get_session

from ..crud import weather_crud
from ..models import (
    WeatherCreate,
    WeatherModel,
)

weather_routes = APIRouter(prefix="/weather", tags=["weather"])


# Rutas
@weather_routes.post("/")  # todo: add response model
def create_weather(weather: WeatherCreate, session: Session = Depends(get_session)):
    weather_db: WeatherModel = weather_crud.create(weather, session)

    return weather_db


@weather_routes.get(
    "/",
    # response_model=List[weatherResponse]
)
def read_weathers(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    db_weathers = weather_crud.get_all(skip, limit, session)
    print(db_weathers)
    return db_weathers


@weather_routes.get("/{weather_id}", response_model=WeatherModel)
def read_weather_by_id(weather_id: int, session: Session = Depends(get_session)):
    weather_db = weather_crud.get_by_id(weather_id, session)
    if not weather_db:
        raise HTTPException(status_code=404, detail="Weather not found")
    return weather_db


@weather_routes.put("/{weather_id}", response_model=WeatherModel)
def update_weather(
    weather_id: int,
    weather_data: WeatherCreate,
    session: Session = Depends(get_session),
):
    # add validation when id is not in db
    # change from put to patch, dont require all the atributes
    # and the update , update_at
    weather_db = weather_crud.update(weather_id, weather_data.model_dump(), session)
    if not weather_db:
        raise HTTPException(status_code=404, detail="Weather not found")
    return weather_db


@weather_routes.delete("/{weather_id}", response_model=WeatherModel)
def delete_weather(weather_id: int, session: Session = Depends(get_session)):
    weather_db = weather_crud.delete(weather_id, session)
    if not weather_db:
        raise HTTPException(status_code=404, detail="Weather not found")
    return weather_db


@weather_routes.get("/count/")
def count_weathers(session: Session = Depends(get_session)):
    response_count = weather_crud.count(session)
    return {"response_count": str(response_count)}
