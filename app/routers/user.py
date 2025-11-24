from typing import Annotated

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlmodel import select

from app.models.user_models import (
    UserPublic,
    UserCreate,
    User,
)
from app.repositories.database import SessionDep
from app.services.requests import get_list
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
    return get_list(session, User, offset=offset, limit=limit)


@router.post("/", response_model=UserCreate)
async def create_user(user: UserCreate, session: SessionDep):
    db_user = User(**user.model_dump())
    email_validate(db_user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user