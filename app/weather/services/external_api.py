import requests

from app.core.config import settings


def fetch_weather_data(
    city_name: str, country_code: str = None, state_code: str = None
) -> dict:
    """
    Fetches weather data for a specific city using the OpenWeatherMap API.

    Args:
        city_name (str): The name of the city for which weather data is to be fetched.
        country_code (str, optional): The country code of the city (default is None).
        state_code (str, optional): The state code of the city (default is None).

    Returns:
        dict: A dictionary containing the weather data for the specified city.

    error message ={
    "cod": "404",
    "message": "city not found"
    }
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    if state_code and country_code:
        query_params = f"{city_name},{state_code},{country_code}"
    elif country_code:
        query_params = f"{city_name},{country_code}"
    else:
        query_params = city_name

    params = {
        "q": query_params,
        "appid": settings.OPEN_WEATHER_API_KEY,
        "units": "metric",
    }

    response = requests.get(base_url, params=params)

    return response.json()
