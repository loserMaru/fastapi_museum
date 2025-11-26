from sqlmodel import select

from app.exceptions.domain import ItemNotFoundError, ValidationError
from app.repositories.database import SessionDep
from app.services.validators import email_validate


def get_list_from_db(session: SessionDep, obj, offset, limit):
    lst = session.exec(select(obj).offset(offset).limit(limit)).all()
    return lst


def get_item_from_db_by_pk(session: SessionDep, obj, item_id):
    item = session.get(obj, item_id)
    if not item:
        raise ItemNotFoundError(f"{obj.__name__} with id={item_id} not found")
    return item


def get_item_from_db(session: SessionDep, obj, column_name: str, value):
    column = getattr(obj, column_name)  # достать нужное поле по имени (эквивалентно записи obj.column_name)
    print(column)
    item = session.exec(select(obj).where(column == value)).first()
    if not item:
        raise ItemNotFoundError(f"{obj.__name__} with column={column_name} and value={value} not found")
    return item


def update_item_from_db(session: SessionDep, obj, item_id, update_data):
    item_db = session.get(obj, item_id)
    if not item_db:
        raise ItemNotFoundError(f"{obj.__name__} with id={item_id} not found")

    item_data = update_data.model_dump(exclude_unset=True)
    item_db.sqlmodel_update(item_data)
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db


def delete_item_from_db(session: SessionDep, obj, item_id):
    item_db = session.get(obj, item_id)
    if not item_db:
        raise ItemNotFoundError(f"{obj.__name__} with id={item_id} not found")
    session.delete(item_db)
    session.commit()
    return {"msg": "Item deleted"}
