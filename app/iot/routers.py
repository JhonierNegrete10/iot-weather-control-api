from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.configDatabase import get_session

from .crud import data_crud, device_crud, setpoints_crud
from .models import (
    DataCreate,
    DataResponse,
    DeviceCreate,
    DeviceResponse,
    SetpointCreate,
    SetpointResponse,
)

device_routes = APIRouter(prefix="/device", tags=["device"])


@device_routes.get("/", response_model=list[DeviceResponse])
def read_devices(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    devices = device_crud.get_all(skip, limit, session)
    return devices


@device_routes.get("/{device_id}", response_model=DeviceResponse)
def read_device(device_id: int, session: Session = Depends(get_session)):
    device = device_crud.get_by_id(device_id, session)
    if device is None:
        raise HTTPException(status_code=404, detail="device not found")
    return device


@device_routes.get("/setpoint/{device_mac}", response_model=SetpointResponse)
def read_last_setpoint(device_mac: str, session: Session = Depends(get_session)):
    device = device_crud.get_by_mac(device_mac, session)
    if device is None:
        raise HTTPException(status_code=404, detail="device not found")

    setpoint = device_crud.get_last_setpoint(device_mac, session)

    return setpoint


@device_routes.post("/", response_model=DeviceResponse)
def create_device(device: DeviceCreate, session: Session = Depends(get_session)):
    device_db = device_crud.get_by_mac(device.mac, session)
    if device_db:
        raise HTTPException(status_code=404, detail="device already created")
    return device_crud.create(device, session)


@device_routes.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int, device: DeviceCreate, session: Session = Depends(get_session)
):
    # add validation device_id and if the mac of device is different in db
    updated_device = device_crud.update(device_id, device, session)
    if updated_device is None:
        raise HTTPException(status_code=404, detail="device not found")
    return updated_device


@device_routes.delete("/{device_id}")
def delete_device(device_id: int, session: Session = Depends(get_session)):
    deleted = delete_device(device_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="device not found")
    return {"message": "device deleted"}


# %% Setpoint Routes
setpoints_routes = APIRouter(prefix="/setpoints", tags=["setpoints"])


@setpoints_routes.get("/", response_model=list[SetpointResponse])
def read_setpoints(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    setpoints = setpoints_crud.get_all(skip, limit, session)
    return setpoints


@setpoints_routes.get("/{setpoint_id}", response_model=SetpointResponse)
def read_setpoint(setpoint_id: int, session: Session = Depends(get_session)):
    setpoint = setpoints_crud.get_by_id(setpoint_id, session)
    if setpoint is None:
        raise HTTPException(status_code=404, detail="Setpoint not found")
    return setpoint


@setpoints_routes.post("/", response_model=SetpointResponse)
def create_setpoint(setpoint: SetpointCreate, session: Session = Depends(get_session)):
    return setpoints_crud.create(setpoint, session)


@setpoints_routes.put("/{setpoint_id}", response_model=SetpointResponse)
def update_setpoint(
    setpoint_id: int,
    setpoint: SetpointCreate,
    session: Session = Depends(get_session),
):
    setpoint = setpoints_crud.update(setpoint_id, setpoint, session)
    if setpoint is None:
        raise HTTPException(status_code=404, detail="Setpoint not found")
    return setpoint


@setpoints_routes.delete("/{setpoint_id}")
def setpoint(setpoint_id: int, session: Session = Depends(get_session)):
    deleted = setpoint(session, setpoint_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Setpoint not found")
    return {"message": "Setpoint deleted"}


# %% Data Routes

data_routes = APIRouter(prefix="/data", tags=["data"])


@data_routes.get("/", response_model=list[DataResponse])
def read_data(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    data_list = data_crud.get_all(skip, limit, session)
    return data_list


@data_routes.get("/{data_id}", response_model=DataResponse)
def read_data_by_id(data_id: int, session: Session = Depends(get_session)):
    data = data_crud.get_by_id(data_id, session)
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return data


@data_routes.post("/", response_model=DataResponse)
def create_data(data: DataCreate, session: Session = Depends(get_session)):
    return data_crud.create(data, session)


@data_routes.put("/{data_id}", response_model=DataResponse)
def update_data(
    data_id: int, data: DataCreate, session: Session = Depends(get_session)
):
    updated_data = data_crud.update(data_id, data, session)
    if updated_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return updated_data


@data_routes.delete("/{data_id}")
def delete_data(data_id: int, session: Session = Depends(get_session)):
    deleted = data_crud.delete(session, data_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"message": "Data deleted"}


# add get data by mac
# add get data by mac  and filtering by date
# posiblemente toque agregar una columna por dia
# ya que extraer todo para extraer el ultimo traiga a todos
