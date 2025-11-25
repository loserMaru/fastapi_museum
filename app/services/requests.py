from fastapi import HTTPException
from sqlmodel import select

from app.exceptions.domain import ItemNotFoundError, ValidationError
from app.repositories.database import SessionDep
from app.services.validators import email_validate


def get_list_from_db(session: SessionDep, obj, offset, limit):
    lst = session.exec(select(obj).offset(offset).limit(limit)).all()
    return lst


def get_item_from_db(session: SessionDep, obj, item_id):
    item = session.get(obj, item_id)
    if not item:
        raise ItemNotFoundError(f"{obj.__name__} with id={item_id} not found")
    return item


def update_item_from_db(session: SessionDep, obj, item_id, update_data):
    item_db = session.get(obj, item_id)
    if not item_db:
        raise ItemNotFoundError(f"{obj.__name__} with id={item_id} not found")

    item_data = update_data.model_dump(exclude_unset=True)

    if "email" in item_data:
        try:
            email_validate(item_data["email"])
        except Exception as e:
            raise ValidationError(str(e))

    item_db.sqlmodel_update(item_data)
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db
