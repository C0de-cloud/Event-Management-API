from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Path, status, Body
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.deps import get_database, get_current_user, get_current_admin_user, pagination_params
from app.crud.user import get_user_by_id, get_users, update_user, delete_user
from app.crud.event import get_user_events, get_user_events_count
from app.models.user import User, UserUpdate, UserPublic
from app.models.event import EventList

router = APIRouter()


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    user_data: Annotated[UserUpdate, Body(...)],
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]
):
    if hasattr(user_data, "role") and user_data.role is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to change your own role"
        )
    
    updated_user = await update_user(db, current_user["id"], user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update user"
        )
    return updated_user


@router.get("/me/events", response_model=EventList)
async def read_users_me_events(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
    pagination: Annotated[dict, Depends(pagination_params)],
    as_organizer: bool = False
):
    user_id = current_user["id"]
    
    events = await get_user_events(
        db, 
        user_id, 
        pagination["limit"], 
        pagination["offset"], 
        as_organizer
    )
    
    total = await get_user_events_count(db, user_id, as_organizer)
    
    return {
        "total": total,
        "limit": pagination["limit"],
        "offset": pagination["offset"],
        "items": events
    }


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(
    user_id: Annotated[str, Path(...)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.get("", response_model=List[UserPublic])
async def read_users(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
    pagination: Annotated[dict, Depends(pagination_params)],
    current_user: Annotated[dict, Depends(get_current_admin_user)]
):
    users = await get_users(
        db, 
        pagination["offset"], 
        pagination["limit"]
    )
    return users


@router.put("/{user_id}", response_model=User)
async def update_user_admin(
    user_id: Annotated[str, Path(...)],
    user_data: Annotated[UserUpdate, Body(...)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]
):
    updated_user = await update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_admin(
    user_id: Annotated[str, Path(...)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]
):
    if current_user["id"] == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return None 