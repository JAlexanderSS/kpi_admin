from pydantic import BaseModel
from datetime import date
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password_hash: str
    date_of_birth: date
    gender: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    date_of_birth: date
    gender: Optional[str]
    is_2fa_enabled: bool

    class Config:
        orm_mode = True
