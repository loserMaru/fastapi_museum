from datetime import datetime, UTC, timezone
from pydantic import field_serializer
from zoneinfo import ZoneInfo

from sqlmodel import SQLModel, Field, Relationship

from app.models.base import TimestampMixin
from app.models.category_model import CategoryPublic


class ExhibitBase(SQLModel):
    title: str = Field(index=True, max_length=50)
    description: str = Field(max_length=500)
    image_url: str = Field(max_length=500)
    category_id: int = Field(foreign_key='category.id', nullable=False)


class Exhibit(ExhibitBase, TimestampMixin, table=True):
    id: int = Field(default=None, primary_key=True)

    # Relationship для ORM
    category: "Category" = Relationship(back_populates="exhibits")  # type: ignore


class ExhibitPublic(ExhibitBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryPublic


    @field_serializer("created_at", "updated_at")
    def serialize(self, value: datetime) -> str:
        moscow = ZoneInfo("Europe/Moscow")

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value.astimezone(moscow).strftime("%d.%m.%Y %H:%M:%S")


class ExhibitCreate(ExhibitBase):
    pass


class ExhibitUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    category_id: int
