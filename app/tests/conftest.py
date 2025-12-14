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
    with Session(engine) as s:
        yield s


# Override зависимости get_session на тестовую сессию
@pytest.fixture(scope="module")
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app) as c:
        yield c


# Создаём тестового пользователя
@pytest.fixture
def test_user(session):
    user = User(
        id=1,
        username="testuser",
        password="12345678",
        email="testmail@gmail.com",
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    yield user
    session.delete(user)
    session.commit()


# Фикстура для авторизации с payload как в основном проекте
@pytest.fixture
def auth_headers(test_user):
    token_data = {"sub": test_user.email}  # как основной проект ожидает
    token = create_access_token(token_data)
    return {"Authorization": f"Bearer {token}"}
