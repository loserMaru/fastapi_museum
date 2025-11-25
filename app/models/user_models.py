from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    username: str = Field(index=True, max_length=25)
    email: str | None = Field(index=True, max_length=50, unique=True)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str = Field(nullable=False)


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    email: str | None = None
    password: str | None = None