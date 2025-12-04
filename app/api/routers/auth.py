from fastapi import APIRouter, HTTPException

from app.exceptions.domain import ItemNotFoundError
from app.models.auth_model import LoginRequest
from app.models.user_models import User
from app.core.database import SessionDep
from app.security.jwt_utils import create_access_token, create_refresh_token
from app.services.requests import get_item_from_db
from app.services.validators import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
        session: SessionDep,
        data: LoginRequest
):
    try:
        user = get_item_from_db(session, User, "email", data.email)

    except ItemNotFoundError:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {
        "access_token": create_access_token({"sub": user.email}),
        "refresh_token": create_refresh_token({"sub": user.email}),
        "token_type": "bearer"
    }
