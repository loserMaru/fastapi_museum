from datetime import datetime, UTC
from sqlalchemy import event
from app.models.base import TimestampMixin

@event.listens_for(TimestampMixin, "before_update", propagate=True)
def update_timestamps(mapper, connection, target):
    target.updated_at = datetime.now(UTC)