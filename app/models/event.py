from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class EventStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELED = "canceled"
    COMPLETED = "completed"


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class Category(CategoryBase):
    id: str
    created_at: datetime
    updated_at: datetime


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    start_date: datetime
    end_date: datetime
    category_id: str
    venue_id: str
    max_attendees: Optional[int] = None
    price: Optional[float] = 0.0
    is_private: bool = False


class EventCreate(EventBase):
    status: EventStatus = EventStatus.DRAFT


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category_id: Optional[str] = None
    venue_id: Optional[str] = None
    max_attendees: Optional[int] = None
    price: Optional[float] = None
    is_private: Optional[bool] = None
    status: Optional[EventStatus] = None


class EventOrganizer(BaseModel):
    id: str
    username: str
    full_name: Optional[str] = None


class EventVenue(BaseModel):
    id: str
    name: str
    address: str
    city: str


class EventCategory(BaseModel):
    id: str
    name: str


class Event(EventBase):
    id: str
    organizer: EventOrganizer
    status: EventStatus
    venue: EventVenue
    category: EventCategory
    attendees_count: int
    created_at: datetime
    updated_at: datetime


class EventList(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[Event]


class EventAttendee(BaseModel):
    event_id: str
    user_id: str
    registered_at: datetime


class EventAttendeeResponse(BaseModel):
    id: str
    username: str
    full_name: Optional[str] = None
    registered_at: datetime 