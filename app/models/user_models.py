from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True)
    password: str = Field()
    email: str | None = Field(index=True)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    username: str | None = None
    email: str | None = None
    password: str | None = None