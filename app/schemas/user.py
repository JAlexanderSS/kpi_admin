from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password_hash: str
    date_of_birth: date
    gender: str
    email: EmailStr  # <-- Nuevo campo comúnmente necesario


class UserOut(BaseModel):
    id: int
    username: str
    date_of_birth: date
    gender: Optional[str]
    is_2fa_enabled: bool
    email: EmailStr  # <-- Incluir también en la salida

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password_hash: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None

class LoginInput(BaseModel):
    email: str
    password: str