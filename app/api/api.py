from fastapi import APIRouter

from app.api.endpoints import auth, users, events, venues, reviews, categories

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(venues.router, prefix="/venues", tags=["venues"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"]) 