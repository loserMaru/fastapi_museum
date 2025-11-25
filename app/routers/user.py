from typing import Annotated

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlmodel import select

from app.exceptions.domain import ItemNotFoundError, ValidationError
from app.models.user_models import (
    UserPublic,
    UserCreate,
    User,
    UserUpdate,
)
from app.repositories.database import SessionDep
from app.services.requests import get_list_from_db, get_item_from_db, update_item_from_db
from app.services.validators import email_validate

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[UserPublic])
async def read(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    return get_list_from_db(session, User, offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(session: SessionDep, user_id: int):
    try:
        return get_item_from_db(session, User, user_id)

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/", response_model=UserCreate)
async def create_user(user: UserCreate, session: SessionDep):
    db_user = User(**user.model_dump())
    email_validate(db_user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch("/{user_id}", response_model=UserUpdate)
async def update_user(session: SessionDep, user_id: int, user_data: UserUpdate):
    try:
        return update_item_from_db(session, User, user_id, user_data)

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
