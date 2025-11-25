from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from passlib.context import CryptContext


def email_validate(email: str):
    try:
        email = validate_email(email, check_deliverability=False)
        email = email.normalized
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return email


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
