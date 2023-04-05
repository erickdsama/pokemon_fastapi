from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, as_declarative, declared_attr

from core.infrastructure.constants import SETTINGS

SQLALCHEMY_DATABASE_URL = f"postgresql://{SETTINGS.db_user}:{SETTINGS.db_password}@{SETTINGS.db_host}/{SETTINGS.db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
