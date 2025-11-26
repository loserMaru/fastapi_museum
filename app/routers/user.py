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
from app.services.requests import (
    get_list_from_db,
    get_item_from_db,
    get_item_from_db_by_pk,
    update_item_from_db,
    delete_item_from_db,
)
from app.services.user_service import UserService
from app.services.validators import email_validate, hash_password

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[UserPublic])
async def get_list(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    return get_list_from_db(session, User, offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(session: SessionDep, user_id: int):
    try:
        return get_item_from_db_by_pk(session, User, user_id)

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/", response_model=UserPublic)
async def create_user(user: UserCreate, session: SessionDep):
    db_user = User(**user.model_dump())
    email_validate(db_user.email)
    try:
        get_item_from_db(session, User, "email", db_user.email)
        raise HTTPException(status_code=400, detail="Email already exists")
    except ItemNotFoundError:
        db_user.password = hash_password(db_user.password)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(session: SessionDep, user_id: int, user_data: UserUpdate):
    try:
        return UserService.update_user(session, user_id, user_data)

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
async def delete_user(session: SessionDep, user_id: int):
    try:
        delete_item_from_db(session, User, user_id)
        return {"msg": f"User with user id {user_id} deleted"}

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
