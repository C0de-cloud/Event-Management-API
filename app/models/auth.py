from pydantic import BaseModel
from typing import Optional

from app.models.user import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None 