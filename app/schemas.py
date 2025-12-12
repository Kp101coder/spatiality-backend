from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class LocationUpdate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class UserResponse(BaseModel):
    id: int
    username: str
    last_latitude: Optional[float] = None
    last_longitude: Optional[float] = None
    last_location_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LocationResponse(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    last_location_time: Optional[datetime] = None

    class Config:
        from_attributes = True
