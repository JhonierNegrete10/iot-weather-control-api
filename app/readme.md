# Documentación de la API Weather Data

La API Weather Data es una aplicación construida con FastAPI que permite interactuar con datos meteorológicos obtenidos de un servicio externo. La aplicación está diseñada para ser ejecutada en contenedores Docker, utilizando Docker Compose para la gestión de la aplicación y la base de datos MySQL.

## Endpoints de la API

### `GET /api/data`

Este endpoint obtiene datos meteorológicos de un servicio externo.

El servicio externo utilizado es una API pública: OpenWeatherMap.

**Parámetros:** No se requieren parámetros, ya que utiliza valores predeterminados para la ubicación. En su defecto, Medellin.

**Respuestas:**

- `200 OK`: Devuelve los datos meteorológicos en un formato estructurado.
- `404 Not Found`: Si la ciudad no se encuentra en la respuesta de la API.

### `POST /api/data`

Este endpoint almacena los datos meteorológicos obtenidos del servicio externo en una base de datos MySQL.

**Parámetros:**

- `weather_api`: Un objeto `WeatherAPIResponse` que contiene los datos meteorológicos a almacenar.

**Respuestas:**

- `200 OK`: Devuelve el objeto `WeatherAPIModel` que representa los datos almacenados en la base de datos.

### `GET /api/data/{id}`

Este endpoint recupera un registro específico de datos meteorológicos de la base de datos MySQL por su ID.

**Parámetros:**

- `id`: El ID del registro de datos meteorológicos a recuperar.

**Respuestas:**

- `200 OK`: Devuelve el objeto `WeatherAPIModel` correspondiente al ID proporcionado.
- `404 Not Found`: Si no se encuentra un registro con el ID proporcionado.

### WebSocket `/ws/data/`

Este endpoint establece una conexión WebSocket que permite ver los datos meteorológicos en tiempo real.

**Parámetros:** No se requieren parámetros.

**Respuestas:**

- Conexión WebSocket establecida para recibir datos en tiempo real.

## Flujo de Información

**Obtención de Datos:** El cliente realiza una solicitud GET a `/api/data` para obtener datos meteorológicos. La API internamente llama a `fetch_and_validate_weather_data` para obtener los datos del servicio externo y los valida.

**Almacenamiento de Datos:** El cliente puede almacenar los datos obtenidos haciendo una solicitud POST a `/api/data` con el objeto `WeatherAPIResponse`. La API utiliza `store_weather_data` para almacenar los datos en la base de datos MySQL.

**Recuperación de Datos:** El cliente puede recuperar un registro específico de datos meteorológicos haciendo una solicitud GET a `/api/data/{id}`. La API utiliza `get_weather_data_by_id` para recuperar los datos de la base de datos.

**Visualización en Tiempo Real:** El cliente puede conectarse al WebSocket en `/ws/data/` para recibir actualizaciones de datos meteorológicos en tiempo real.

## Almacenamiento de Datos

Los datos meteorológicos obtenidos del servicio externo se almacenan en una tabla en la base de datos MySQL. La estructura de la tabla y los modelos de datos están definidos en `weather/models.py`
