from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ReviewBase(BaseModel):
    event_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=1, max_length=1000)

    @validator("rating")
    def rating_range(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=1, max_length=1000)


class ReviewAuthor(BaseModel):
    id: str
    username: str
    full_name: Optional[str] = None


class Review(ReviewBase):
    id: str
    author: ReviewAuthor
    created_at: datetime
    updated_at: datetime


class ReviewList(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[Review]


class EventRatingSummary(BaseModel):
    average_rating: float
    ratings_count: int
    ratings_distribution: dict 