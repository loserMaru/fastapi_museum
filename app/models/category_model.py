from sqlmodel import SQLModel, Field, Relationship


class CategoryBase(SQLModel):
    title: str = Field(index=True, nullable=False, unique=True)
    description: str = Field(max_length=255)


class Category(CategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    exhibits: list["Exhibit"] = Relationship(back_populates="category")  # type: ignore


class CategoryPublic(CategoryBase):
    id: int


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
