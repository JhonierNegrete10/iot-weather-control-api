from fastapi import APIRouter

from app.utils.base_crud import BaseCRUD  # noqa: F401

from .models import DataModel, DeviceModel, SetpointModel  # noqa: F401
from .routers import data_routes, device_routes, setpoints_routes  # noqa: F401

iot_router = APIRouter()
iot_router.include_router(device_routes)
iot_router.include_router(setpoints_routes)
iot_router.include_router(data_routes)
