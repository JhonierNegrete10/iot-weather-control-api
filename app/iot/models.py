from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from app.utils.data_time_zone import DateTimeColombia


# Definición del Enum para el estado de la válvula
class ValveStatus(str, Enum):
    ON = "ON"
    OFF = "OFF"


# Clase base que contiene los campos comunes
class BaseTable(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=DateTimeColombia.now, index=True)
    updated_at: datetime = Field(default_factory=DateTimeColombia.now)
    created_date: date = Field(default_factory=DateTimeColombia.today)


# Definición del modelo device
class DeviceModel(BaseTable, table=True):
    device_mac: str = Field(unique=True, nullable=False, index=True)
    description: str
    setpoints: list["SetpointModel"] = Relationship(back_populates="device")
    data: list["DataModel"] = Relationship(back_populates="device")


class Device(BaseModel):
    device_mac: str
    description: str
    setpoints: list["SetpointModel"]


class DeviceResponse(BaseModel):
    id: int
    device_mac: str
    description: str


class DeviceCreate(BaseModel):
    device_mac: str
    description: str


class DeviceUpdate(BaseModel):
    device_mac: Optional[str]
    description: Optional[str]


# Definición del modelo HistoricoSetpoint
class SetpointModel(BaseTable, table=True):
    setpoint: float
    device_mac: str = Field(foreign_key="devicemodel.device_mac", index=True)
    device: DeviceModel = Relationship(back_populates="setpoints")


class SetpointCreate(BaseModel):
    setpoint: float
    device_mac: str


class SetpointResponse(BaseModel):
    id: int
    created_at: datetime
    setpoint: float
    device_mac: str


# Definición del modelo Data
class DataModel(BaseTable, table=True):
    device_mac: str = Field(foreign_key="devicemodel.device_mac", index=True)
    temperature: float
    humidity_1: float
    humidity_2: float
    valve_status: ValveStatus
    device: DeviceModel = Relationship(back_populates="data")


class DataCreate(BaseModel):
    temperature: float
    humidity_1: float
    humidity_2: float
    valve_status: ValveStatus
    device_mac: str


class DataResponse(BaseModel):
    id: int
    created_at: datetime
    created_date: date
    temperature: float
    humidity_1: float
    humidity_2: float
    valve_status: ValveStatus
    device_mac: str
