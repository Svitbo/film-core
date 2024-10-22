from fastapi import FastAPI

from .routes import film_router, user_router

app = FastAPI()

app.include_router(film_router, prefix="/films", tags=["films"])
app.include_router(user_router, tags=["users"])
