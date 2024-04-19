# SQLModel based on pydantic and SQLalchemy
import logging
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

log = logging.getLogger("uvicorn")

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Return all doing in the db
    future=True,
    pool_pre_ping=True,
    isolation_level="AUTOCOMMIT",
    # query_cache_size=0,
    # expire_on_commit=True,
    # execution_options={"compiled_cache": None, "autocomit": True},
)


def init_db():
    """
    initialization of the database sync
    """
    global engine
    try:
        # SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"{__name__}: An exception occurred {e}")


def get_session() -> Generator:
    try:
        with Session(engine) as session:
            yield session
    finally:
        session.close()
