from .film_routes import router as film_router
from .review_routes import router as review_router
from .user_routes import router as user_router

__all__ = ["user_router", "film_router", "review_router"]
