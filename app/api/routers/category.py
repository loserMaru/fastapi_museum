from typing import Annotated

from fastapi import APIRouter, Query, HTTPException

from app.exceptions.domain import ItemNotFoundError
from app.models.category_model import Category, CategoryPublic, CategoryCreate, CategoryUpdate
from app.core.database import SessionDep
from app.services.requests import get_list_from_db, get_item_from_db, get_item_from_db_by_pk, update_item_from_db, \
    delete_item_from_db

router = APIRouter(
    prefix="/category",
    tags=["category"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[CategoryPublic])
async def get_list(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    return get_list_from_db(session, Category, offset, limit)


@router.post("/", response_model=CategoryPublic)
async def create_category(session: SessionDep, category: CategoryCreate):
    db_category = Category(**category.model_dump())
    try:
        get_item_from_db(session, Category, "title", db_category.title)
        raise HTTPException(status_code=400, detail="Category already exists")

    except ItemNotFoundError:
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category


@router.get("/{category_id}", response_model=CategoryPublic)
async def get_category(session: SessionDep, category_id: int):
    try:
        return get_item_from_db_by_pk(session, Category, category_id)

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")


@router.patch("/{category_id}", response_model=CategoryPublic)
async def update_category(session: SessionDep, category_id: int, category_data: CategoryUpdate):
    try:
        return update_item_from_db(session, Category, category_id, category_data)

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/{category_id")
async def delete_category(session: SessionDep, category_id: int):
    try:
        delete_item_from_db(session, Category, category_id)
        return {"msg": f"Category with id {category_id} deleted successfully"}

    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")
