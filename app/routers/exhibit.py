import uuid
from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, Query, HTTPException, Form, File, UploadFile

from app.exceptions.domain import ItemNotFoundError
from app.models.category_model import Category
from app.models.exhibit_model import Exhibit, ExhibitPublic
from app.repositories.database import SessionDep
from app.services.exhibit_service import ExhibitService
from app.services.requests import (
    get_list_from_db,
    get_item_from_db_by_pk,
    delete_item_from_db,
    get_item_from_db
)

router = APIRouter(
    prefix="/exhibit",
    tags=["exhibit"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ExhibitPublic])
async def get_list(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    return get_list_from_db(session, Exhibit, offset, limit)


@router.get("/{exhibit_id}", response_model=ExhibitPublic)
async def get_exhibit(session: SessionDep, exhibit_id: int):
    return get_item_from_db_by_pk(session, Exhibit, exhibit_id)


@router.post("/", response_model=ExhibitPublic)
async def create_exhibit(
        session: SessionDep,
        title: str = Form(...),
        description: str = Form(...),
        category_id: int = Form(...),
        image: UploadFile | None = File(None),
):
    try:
        get_item_from_db(session, Category, "id", category_id)

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")

    image_url = None
    if image:
        UPLOAD_DIR = Path("app/static/uploads")
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        ext = image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = UPLOAD_DIR / filename

        with filepath.open("wb") as buffer:
            buffer.write(await image.read())

        image_url = f"app/static/uploads/{filename}"

    db_exhibit = Exhibit(
        title=title,
        description=description,
        category_id=category_id,
        image_url=image_url,
    )

    session.add(db_exhibit)
    session.commit()
    session.refresh(db_exhibit)
    return db_exhibit


@router.patch("/{exhibit_id}", response_model=ExhibitPublic)
async def update_exhibit(
        session: SessionDep,
        exhibit_id: int,
        title: str | None = Form(None),
        description: str | None = Form(None),
        category_id: int | None = Form(None),
        image: UploadFile | None = File(None),
):
    return ExhibitService.update_exhibit(
        session,
        exhibit_id,
        title,
        description,
        category_id,
        image
    )


@router.delete("/{exhibit_id}")
async def delete_exhibit(session: SessionDep, exhibit_id: int):
    try:
        delete_item_from_db(session, Exhibit, exhibit_id)
        return {"msg": f"Item with id {exhibit_id} successfully deleted"}

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
