import uuid
from pathlib import Path

from fastapi import HTTPException

from app.models.category_model import Category
from app.models.exhibit_model import Exhibit
from app.services.requests import get_item_from_db_by_pk, get_item_from_db


class ExhibitService:

    @staticmethod
    def update_exhibit(session, exhibit_id, title, description, category_id, image):
        exhibit = get_item_from_db_by_pk(session, Exhibit, exhibit_id)

        if not exhibit:
            raise HTTPException(status_code=404, detail="Exhibit not found")

        if category_id is not None:
            category = get_item_from_db(session, Category, "id", category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            exhibit.category_id = category_id

        if title is not None:
            exhibit.title = title

        if description is not None:
            exhibit.description = description

        if image is not None:
            if exhibit.image_url:
                old_path = Path(exhibit.image_url)
                if old_path.exists():
                    old_path.unlink()

            ext = image.filename.split(".")[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            filepath = Path("app/static/uploads") / filename

            with filepath.open("wb") as buffer:
                buffer.write(image.file.read())

            exhibit.image_url = f"app/static/uploads/{filename}"

        session.add(exhibit)
        session.commit()
        session.refresh(exhibit)
        return exhibit
