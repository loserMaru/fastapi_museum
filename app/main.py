from fastapi import FastAPI

from app.core.database import create_db_and_tables
from app.repositories.timestamps import update_timestamps  # type: ignore
from app.api.routers import user, view_history
from app.api.routers import auth, category, exhibit

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(exhibit.router)
app.include_router(view_history.router)
