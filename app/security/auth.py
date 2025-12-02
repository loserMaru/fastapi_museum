from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.user_models import User
from app.core.database import SessionDep
from app.security.jwt_utils import decode_token
from app.services.requests import get_item_from_db

bearer_scheme = HTTPBearer()  # извлекает токен из заголовка Authorization


def get_current_user(
        session: SessionDep,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials
    payload = decode_token(token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    # user = session.exec(select(User).where(User.email == email)).first()
    user = get_item_from_db(session, User, "email", email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
