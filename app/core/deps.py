from typing import Annotated, Dict, Optional
from jose import JWTError, jwt
from datetime import datetime

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import get_settings
from app.db.mongodb import get_database
from app.models.user import UserRole
from app.crud.user import get_user_by_id

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]
) -> Dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_admin_user(
    current_user: Annotated[Dict, Depends(get_current_user)]
) -> Dict:
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_current_organizer_or_admin_user(
    current_user: Annotated[Dict, Depends(get_current_user)]
) -> Dict:
    if current_user["role"] not in [UserRole.ORGANIZER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


async def pagination_params(
    limit: Annotated[int, Query(10, ge=1, le=100)],
    offset: Annotated[int, Query(0, ge=0)]
) -> Dict:
    return {"limit": limit, "offset": offset}


async def event_filter_params(
    status: Annotated[Optional[str], Query(None)],
    category_id: Annotated[Optional[str], Query(None)],
    venue_id: Annotated[Optional[str], Query(None)],
    min_date: Annotated[Optional[datetime], Query(None)],
    max_date: Annotated[Optional[datetime], Query(None)],
    organizer_id: Annotated[Optional[str], Query(None)],
    is_free: Annotated[Optional[bool], Query(None)],
    search: Annotated[Optional[str], Query(None)]
) -> Dict:
    filters = {}
    if status:
        filters["status"] = status
    if category_id:
        filters["category_id"] = category_id
    if venue_id:
        filters["venue_id"] = venue_id
    if min_date:
        filters["start_date"] = {"$gte": min_date}
    if max_date:
        if "start_date" in filters:
            filters["start_date"]["$lte"] = max_date
        else:
            filters["start_date"] = {"$lte": max_date}
    if organizer_id:
        filters["organizer_id"] = organizer_id
    if is_free is not None:
        if is_free:
            filters["price"] = 0
        else:
            filters["price"] = {"$gt": 0}
    if search:
        filters["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    return filters


async def venue_filter_params(
    city: Annotated[Optional[str], Query(None)],
    country: Annotated[Optional[str], Query(None)],
    min_capacity: Annotated[Optional[int], Query(None)],
    search: Annotated[Optional[str], Query(None)]
) -> Dict:
    filters = {}
    if city:
        filters["city"] = {"$regex": city, "$options": "i"}
    if country:
        filters["country"] = {"$regex": country, "$options": "i"}
    if min_capacity:
        filters["capacity"] = {"$gte": min_capacity}
    if search:
        filters["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"address": {"$regex": search, "$options": "i"}}
        ]
    return filters 