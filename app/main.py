from fastapi import FastAPI

from app.repositories.database import create_db_and_tables
from app.repositories.timestamps import update_timestamps  # type: ignore
from app.routers import user, category, exhibit, auth

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(user.router)
app.include_router(category.router)
app.include_router(exhibit.router)
app.include_router(auth.router)
