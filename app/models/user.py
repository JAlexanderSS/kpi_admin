from sqlalchemy import Column, Integer, String, Date, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10))
    otp_secret = Column(String)
    is_2fa_enabled = Column(Boolean, default=False)
