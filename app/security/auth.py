from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user_models import User
from app.repositories.database import SessionDep
from app.security.jwt_utils import create_access_token
from app.services.requests import get_item_from_db
from app.services.validators import verify_password

router = APIRouter()

@router.post("/login")
async def login(login_data: LoginRequest, session: SessionDep):
    user = get_item_from_db(session, User, "email", login_data.email)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}