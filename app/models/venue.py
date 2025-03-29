from typing import Optional, List, Tuple
from pydantic import BaseModel, Field
from datetime import datetime


class GeoLocation(BaseModel):
    type: str = "Point"
    coordinates: Tuple[float, float]  # [longitude, latitude]


class VenueBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    country: str = Field(..., min_length=2)
    postal_code: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    amenities: List[str] = Field(default_factory=list)
    location: Optional[GeoLocation] = None


class VenueCreate(VenueBase):
    pass


class VenueUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = Field(None, min_length=1)
    city: Optional[str] = Field(None, min_length=1)
    country: Optional[str] = Field(None, min_length=2)
    postal_code: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    amenities: Optional[List[str]] = None
    location: Optional[GeoLocation] = None


class Venue(VenueBase):
    id: str
    created_at: datetime
    updated_at: datetime


class VenueList(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[Venue] 