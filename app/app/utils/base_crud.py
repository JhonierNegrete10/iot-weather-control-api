from datetime import date
from typing import List, Type

from sqlmodel import Session, SQLModel, func, select


class BaseCRUD:
    def __init__(self):
        self.model: SQLModel

    def create(self, obj: SQLModel, session: Session):
        db_obj = self.model(**obj.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_all(self, skip, limit, session: Session) -> List[SQLModel]:
        statement = select(self.model).offset(skip).limit(limit)
        result = session.exec(statement)
        result = result.all()
        return [obj_db for obj_db in result]

    def get_by_id(self, id, session: Session) :
        statement = select(self.model).where(self.model.id == id)
        result = session.exec(statement)
        obj = result.first()
        return obj

    def update(self, id, obj_data, session: Session):
        obj_data = obj_data.model_dump()
        statement = select(self.model).where(self.model.id == id)
        result = session.exec(statement)
        db_obj = result.first()
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def delete(self, id, session: Session):
        statement = select(self.model).where(self.model.id == id)
        result = session.exec(statement)
        db_obj = result.first()
        session.delete(db_obj)
        session.commit()
        return db_obj

    def count(self, session: Session) -> int:
        statement = select(func.count()).select_from(self.model)
        result = session.exec(statement)
        count = result.first()
        return count

    def filter_by(self, filters: dict, session: Session) -> List[SQLModel]:
        statement = select(self.model).where(**filters)
        result = session.exec(statement)
        result = result.all()
        return [obj_db for obj_db in result]

    @staticmethod
    def filter_data_by_date_and_attribute(
        session: Session, model: Type, date_value: date, **attributes
    ) -> List:
        """
        Filtra los datos en la base de datos por una fecha y otros atributos específicos.

        :param session: Instancia de la sesión de SQLAlchemy.
        :param model: Clase del modelo SQLAlchemy.
        :param date_value: Fecha específica para filtrar los datos.
        :param attributes: Diccionario de atributos adicionales para filtrar.
        :return: Lista de objetos filtrados por la fecha y los atributos especificados.
        """
        query = session.query(model).filter(model.created_date == date_value)
        for attr, value in attributes.items():
            query = query.filter(getattr(model, attr) == value)
        result = query.all()
        return result
