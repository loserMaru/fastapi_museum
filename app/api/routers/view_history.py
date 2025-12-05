from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.database import SessionDep
from app.models.user_models import User
from app.models.view_history_model import ViewHistoryPublic, ViewHistory
from app.security.auth import get_current_user
from app.services.requests import get_list_from_db
from app.services.view_history_service import ViewHistoryService

router = APIRouter(
    prefix="/view-history",
    tags=["view-history"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=list[ViewHistoryPublic])
async def get_view_history(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
        user: User = Depends(get_current_user)
):
    return ViewHistoryService.get_user_view_history(session, user.id, offset, limit)
