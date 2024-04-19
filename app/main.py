# main.py

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from iot import DataModel, DeviceModel, SetpointModel, iot_router  # noqa: F401
from weather import WeatherAPIModel, api_router  # noqa: F401

from app.core.config import settings
from app.db.configDatabase import init_db

logging.basicConfig(
    filename="app.log",
    # filemode='w',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


log = logging.getLogger("uvicorn")

# Configuración de FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=""" IOT WEATHER API CONTROL """,
)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(iot_router)


@app.get("/")
def home():
    return {
        "Welcome": dict(
            title=settings.PROJECT_NAME,
            version=settings.PROJECT_VERSION,
            description=""" IOT WEATHER API CONTROL """,
        )
    }


@app.on_event("startup")
async def startup_event():
    log.info("INIT: ___Starting up___")
    try:
        init_db()
    except Exception as e:
        print(f"An exception occurred {e}")

    log.info("INIT: ___end___")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
