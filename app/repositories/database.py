from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

from app.models.category_model import Category  # type: ignore
from app.models.exhibit_model import Exhibit  # type: ignore
from app.models.user_models import User  # type: ignore

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
