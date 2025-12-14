import uuid

import pytest

from sqlalchemy import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from starlette.testclient import TestClient

from app.main import app
from app.models.user_models import User
from app.core.database import get_session
from app.security.jwt_utils import create_access_token

# In-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

# Создаём все таблицы один раз
SQLModel.metadata.create_all(bind=engine)


# Фикстура сессии для всех тестов
@pytest.fixture(scope="module")
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# Override зависимости get_session на тестовую сессию
@pytest.fixture()
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Создаём тестового пользователя
@pytest.fixture
def test_user(session):
    user = User(
        username=f"testuser_{uuid.uuid4().hex[:6]}",
        password="12345678",
        email=f"test_{uuid.uuid4().hex[:6]}@gmail.com",
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Фикстура для авторизации с payload как в основном проекте
@pytest.fixture
def auth_headers(test_user):
    token_data = {"sub": test_user.email}  # как основной проект ожидает
    token = create_access_token(token_data)
    return {"Authorization": f"Bearer {token}"}
