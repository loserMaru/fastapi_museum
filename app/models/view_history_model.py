from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from pydantic import field_serializer
from sqlmodel import SQLModel, Field, Relationship

from app.models.exhibit_model import ExhibitPublic


class ViewHistoryBase(SQLModel):
    user_id: int = Field(foreign_key="user.id", nullable=False)
    exhibit_id: int = Field(foreign_key="exhibit.id", nullable=False)
    viewed_at: datetime = Field(default_factory=datetime.utcnow)


class ViewHistory(ViewHistoryBase, table=True):
    id: int = Field(default=None, primary_key=True)

    user: "User" = Relationship(back_populates="viewhistory")  # type: ignore
    exhibits: "Exhibit" = Relationship(back_populates="viewhistory")  # type: ignore


class ViewHistoryPublic(SQLModel):
    id: int
    viewed_at: datetime
    exhibit: ExhibitPublic

    @field_serializer("viewed_at")
    def serialize(self, value: datetime) -> str:
        moscow = ZoneInfo("Europe/Moscow")

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value.astimezone(moscow).strftime("%d.%m.%Y %H:%M:%S")