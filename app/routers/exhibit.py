from typing import Annotated

from fastapi import APIRouter, Query, HTTPException

from app.exceptions.domain import ItemNotFoundError
from app.models.category_model import Category
from app.models.exhibit_model import Exhibit, ExhibitPublic, ExhibitCreate, ExhibitUpdate
from app.repositories.database import SessionDep
from app.services.exhibit_service import ExhibitService
from app.services.requests import get_list_from_db, get_item_from_db_by_pk, update_item_from_db, delete_item_from_db, \
    get_item_from_db

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
async def create_exhibit(session: SessionDep, exhibit: ExhibitCreate):
    db_exhibit = Exhibit(**exhibit.model_dump())
    try:
        get_item_from_db(session, Category, "id", exhibit.category_id)

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")

    session.add(db_exhibit)
    session.commit()
    session.refresh(db_exhibit)
    return db_exhibit


@router.patch("/{exhibit_id}", response_model=ExhibitPublic)
async def update_exhibit(session: SessionDep, exhibit_id: int, exhibit_data: ExhibitUpdate):
    return ExhibitService.update_exhibit(session, exhibit_id, exhibit_data)


@router.delete("/{exhibit_id}")
async def delete_exhibit(session: SessionDep, exhibit_id: int):
    try:
        delete_item_from_db(session, Exhibit, exhibit_id)
        return {"msg": f"Item with id {exhibit_id} successfully deleted"}

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
