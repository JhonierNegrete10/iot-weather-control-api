from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from app.utils.data_time_zone import DateTimeColombia


class BaseTableModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=DateTimeColombia.now)
    updated_at: datetime = Field(default_factory=DateTimeColombia.now)
    created_date: date = Field(default_factory=DateTimeColombia.today)


class WeatherModel(BaseTableModel, table=True):
    city_name: str
    temperature: float
    description: str


class WeatherCreate(BaseModel):
    city_name: str
    temperature: float
    description: str


class WeatherAPIResponse(BaseModel):
    city_name: str
    city_id: str
    temperature: float
    pressure: float
    description: str
    icon: str
    lon: float
    lat: float
    weather_api_id: str
    humidity: float
    wind_speed: float
    wind_deg: float
    country: str


class WeatherAPIModel(BaseTableModel, WeatherAPIResponse, table=True):
    pass


###########
class LocationParams(SQLModel):
    city_name: str = Field(default="Medellin")
    country_code: str | None = Field(default="")
    state_code: str | None = Field(default="")


class Coord(SQLModel):
    lon: float
    lat: float


class Weather(SQLModel):
    id: int
    main: str
    description: str
    icon: str


class Main(SQLModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class Wind(SQLModel):
    speed: float
    deg: int


class Clouds(SQLModel):
    all: int


class Sys(SQLModel):
    type: int
    id: int
    country: str
    sunrise: int
    sunset: int


class WeatherData(SQLModel):
    coord: Coord
    weather: List[Weather]
    base: str
    main: Main
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int
