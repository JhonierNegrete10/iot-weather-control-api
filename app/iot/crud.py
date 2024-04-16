# from sqlalchemy.orm import selectinload
from operator import attrgetter

from sqlmodel import Session, select

from app.utils.base_crud import BaseCRUD

from .models import DataModel, DeviceModel, SetpointModel


class DeviceCRUD(BaseCRUD):
    model = DeviceModel

    def get_by_mac(self, mac, session: Session):
        statement = select(self.model).where(self.model.mac == mac)
        result = session.exec(statement)
        obj = result.first()
        return obj

    def get_setpoints(self, mac, session: Session):
        statement = select(self.model).where(self.model.mac == mac)
        result = session.exec(statement)
        obj = result.first()
        if obj:
            return obj.setpoints
        return None

    def get_last_setpoint(self, mac, session: Session):
        setpoints: list = self.get_setpoints(mac, session)
        if not setpoints:
            return None
        setpoints = sorted(setpoints, key=attrgetter("created_at"), reverse=True)
        return setpoints[0]


device_crud = DeviceCRUD()


class SetpointsCRUD(BaseCRUD):
    model = SetpointModel


setpoints_crud = SetpointsCRUD()


class DataCRUD(BaseCRUD):
    model = DataModel

    def get_by_mac(self, mac, session: Session):
        statement = select(self.model).where(self.model.mac == mac)
        result = session.exec(statement)
        obj = result.first()
        return obj


data_crud = DataCRUD()
