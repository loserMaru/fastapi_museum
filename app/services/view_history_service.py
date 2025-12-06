import json

from app.core.redis import redis_client
from app.models.view_history_model import ViewHistory
from app.services.requests import get_list_from_db, get_list_from_db_with_params


class ViewHistoryService:

    @staticmethod
    def get_view_history_list(session, offset, limit):
        """
        Обычный метод без фильтрации по пользователю.
        (Можно также закешировать, если нужно)
        """
        view_histories = get_list_from_db(session, ViewHistory, offset, limit)

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

    @staticmethod
    def get_user_view_history(session, user_id: int, offset: int, limit: int):
        cache_key = f"view_history:{user_id}:{offset}:{limit}"

        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        view_histories = get_list_from_db_with_params(
            session,
            ViewHistory,
            "user_id",
            user_id,
            offset,
            limit
        )

        data = []
        for vh in view_histories:
            item = vh.model_dump()

            # ------------ важное исправление ------------
            # viewed_at является datetime => нужно вручную превратить в строку
            item["viewed_at"] = vh.viewed_at.isoformat()
            # --------------------------------------------

            exhibit = vh.exhibits
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

        redis_client.setex(cache_key, 600, json.dumps(data))
        return data

    @staticmethod
    def invalidate_user_cache(user_id: int):
        """
        Удаляет ВСЕ кэши для этого пользователя (любые offset/limit).
        Простой вариант через SCAN.
        Работает синхронно.
        """
        pattern = f"view_history:{user_id}:*"
        for key in redis_client.scan_iter(pattern):
            redis_client.delete(key)
