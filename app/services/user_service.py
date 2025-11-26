from app.exceptions.domain import ValidationError
from app.models.user_models import User, UserUpdate
from app.services.requests import update_item_from_db
from app.services.validators import hash_password, email_validate


class UserService:

    @staticmethod
    def validate_update(user: UserUpdate) -> UserUpdate:
        if user.email:
            try:
                email_validate(user.email)
            except Exception as e:
                raise ValidationError(str(e))

        if user.password:
            user.password = hash_password(user.password)

        return user

    @staticmethod
    def update_user(session, user_id, user_data):

        validated = UserService.validate_update(user_data)

        return update_item_from_db(session, User, user_id, validated)
