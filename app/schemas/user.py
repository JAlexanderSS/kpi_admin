from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password_hash: str
    date_of_birth: date
    gender: str
    email: EmailStr


class UserOut(BaseModel):
    id: int
    username: str
    date_of_birth: date
    gender: Optional[str]
    is_2fa_enabled: bool
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password_hash: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    is_2fa_enabled: Optional[bool] = None  # Opcional para habilitar 2FA
    otp_secret: Optional[str] = None       # Para actualizar secreto si lo deseas


class LoginInput(BaseModel):
    email: EmailStr
    password: str
    otp_code: Optional[str] = None  # ✅ Este campo es clave para 2FA
