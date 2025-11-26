from datetime import datetime, UTC

from sqlmodel import SQLModel, Field, Relationship

from app.models.category_model import CategoryPublic


class ExhibitBase(SQLModel):
    title: str = Field(index=True, max_length=50)
    description: str = Field(max_length=500)
    image_url: str = Field(max_length=500)
    category_id: int = Field(foreign_key='category.id', nullable=False)


class Exhibit(ExhibitBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationship для ORM
    category: "Category" = Relationship(back_populates="exhibits")  # type: ignore


class ExhibitPublic(ExhibitBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryPublic


class ExhibitCreate(ExhibitBase):
    pass


class ExhibitUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    category_id: int | None = None
