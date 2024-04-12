from fastapi import APIRouter

from app.utils.base_crud import BaseCRUD  # noqa: F401

from .models import WeatherAPIModel, WeatherModel  # noqa: F401
from .routers import api_routers  # noqa: F401

api_router = APIRouter()
api_router.include_router(api_routers)
