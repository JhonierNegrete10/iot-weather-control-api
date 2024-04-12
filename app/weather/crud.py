from app.utils.base_crud import BaseCRUD

from .models import WeatherAPIModel, WeatherModel


class WeatherCRUD(BaseCRUD):
    model = WeatherModel


weather_crud = WeatherCRUD()


class WeatherAPICRUD(BaseCRUD):
    model = WeatherAPIModel


weather_api_crud = WeatherAPICRUD()
