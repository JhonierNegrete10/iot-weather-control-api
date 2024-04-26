# from sqlalchemy.orm import selectinload
from operator import attrgetter

from sqlmodel import Session, select

from app.utils.base_crud import BaseCRUD
from app.utils.data_time_zone import DateTimeColombia

from .models import DataModel, DeviceModel, SetpointModel


class GetMACCRUD(BaseCRUD):
    def get_by_mac(self, device_mac, session: Session):
        statement = select(self.model).where(self.model.device_mac == device_mac)
        result = session.exec(statement)
        obj = result.first()
        return obj


class DeviceCRUD(GetMACCRUD):
    model = DeviceModel

    def get_setpoints(self, device_mac, session: Session):
        statement = select(self.model).where(self.model.device_mac == device_mac)
        result = session.exec(statement)
        obj = result.first()
        if obj:
            return obj.setpoints
        return None

    def get_last_setpoint(self, device_mac, session: Session):
        setpoints: list = self.get_setpoints(device_mac, session)
        if not setpoints:
            return None
        setpoints = sorted(setpoints, key=attrgetter("created_at"), reverse=True)
        return setpoints[0]


device_crud = DeviceCRUD()


class SetpointsCRUD(GetMACCRUD):
    model = SetpointModel


setpoints_crud = SetpointsCRUD()


class DataCRUD(GetMACCRUD):
    model = DataModel

    def get_all_by_mac(self, device_mac, session: Session):
        statement = select(self.model).where(self.model.device_mac == device_mac)
        result = session.exec(statement)
        result = result.all()
        return [obj_db for obj_db in result]

    def filter_data_current_day(self, skip, limit, device_mac: str, session: Session):
        current_date = DateTimeColombia.today()

        statement = (
            select(self.model)
            .where(
                self.model.device_mac == device_mac,
                self.model.created_date == current_date,
            )
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = session.exec(statement)
        return [obj_db for obj_db in result]


data_crud = DataCRUD()
