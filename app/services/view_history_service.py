from sqlalchemy.util.langhelpers import repr_tuple_names

from app.core.database import SessionDep
from app.models.view_history_model import ViewHistory
from app.services.requests import get_list_from_db, get_list_from_db_with_params


class ViewHistoryService:
    @staticmethod
    def get_view_history_list(session, offset, limit):
        view_histories = get_list_from_db(session, ViewHistory, offset, limit)

        data = []
        for view_history in view_histories:
            item = view_history.model_dump()  # базовые поля ViewHistory

            exhibit = view_history.exhibits  # ORM объект
            item["exhibit"] = {
                "id": exhibit.id,
                "title": exhibit.title,
                "description": exhibit.description,
                "category_id": exhibit.category_id,  # <-- добавляем
                "image_url": exhibit.image_url,
                "created_at": exhibit.created_at.isoformat(),
                "updated_at": exhibit.updated_at.isoformat(),
                "category": {
                    "id": exhibit.category.id,
                    "title": exhibit.category.title,
                    "description": exhibit.category.description,
                }
            }

            data.append(item)

        return data

    @staticmethod
    def get_user_view_history(session, user_id: int, offset: int, limit: int):
        """
        Возвращает историю просмотра только для конкретного пользователя.
        """
        # Фильтруем записи по user_id
        view_histories = get_list_from_db_with_params(
            session, ViewHistory,
            "user_id",
            user_id,
            offset,
            limit
        )

        data = []
        for view_history in view_histories:
            item = view_history.model_dump()

            exhibit = view_history.exhibits
            item["exhibit"] = {
                "id": exhibit.id,
                "title": exhibit.title,
                "description": exhibit.description,
                "category_id": exhibit.category_id,
                "image_url": exhibit.image_url,
                "created_at": exhibit.created_at.isoformat(),
                "updated_at": exhibit.updated_at.isoformat(),
                "category": {
                    "id": exhibit.category.id,
                    "title": exhibit.category.title,
                    "description": exhibit.category.description,
                }
            }

            data.append(item)

        return data
