from fastapi import HTTPException

from app.models.category_model import Category
from app.models.exhibit_model import Exhibit, ExhibitUpdate
from app.repositories.database import SessionDep
from app.services.requests import get_item_from_db, update_item_from_db


class ExhibitService:

    @staticmethod
    def update_exhibit(session: SessionDep, exhibit_id: int, exhibit_data: ExhibitUpdate) -> Exhibit:
        # Проверка существования категории, если передан category_id
        if exhibit_data.category_id is not None:
            category = get_item_from_db(session, Category, "id", exhibit_data.category_id)
            if not category:
                raise HTTPException(
                    status_code=404,
                    detail=f"Category with id {exhibit_data.category_id} not found"
                )

        # Получаем и обновляем экспонат
        updated_exhibit = update_item_from_db(session, Exhibit, exhibit_id, exhibit_data)
        if not updated_exhibit:
            raise HTTPException(
                status_code=404,
                detail=f"Exhibit with id {exhibit_id} not found"
            )

        return updated_exhibit