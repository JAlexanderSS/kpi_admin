from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, UserOut, UserUpdate, LoginInput
from app.models.user_oracle import UserOracle
from app.db.oracle import SessionLocalOracle
from app.utils.otp import generate_otp_secret, generate_qr_code
import pyotp
from app.auth.jwt_handler import create_access_token


router = APIRouter()

def get_db():
    db = SessionLocalOracle()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=dict)
def create_user_oracle(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserOracle).filter(UserOracle.username == user.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe en Oracle")

    otp_secret = generate_otp_secret()
    new_user = UserOracle(**user.dict(), otp_secret=otp_secret, is_2fa_enabled=False)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    qr_code = generate_qr_code(new_user.username, new_user.email, otp_secret)

    return {
        "user": UserOut.model_validate(new_user),
        "qr_code_base64": qr_code
    }


@router.get("/", response_model=List[UserOut])
def get_users_oracle(db: Session = Depends(get_db)):
    return db.query(UserOracle).all()


@router.get("/{user_id}", response_model=UserOut)
def get_user_oracle(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserOracle).filter(UserOracle.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user_oracle(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserOracle).filter(UserOracle.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en Oracle")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", response_model=dict)
def delete_user_oracle(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserOracle).filter(UserOracle.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en Oracle")

    db.delete(user)
    db.commit()
    return {"message": f"Usuario con ID {user_id} eliminado correctamente"}


@router.post("/validate-login")
def validate_login(credentials: LoginInput, db: Session = Depends(get_db)):
    user = db.query(UserOracle).filter(UserOracle.email == credentials.email).first()

    if not user or user.password_hash != credentials.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if user.is_2fa_enabled:
        if not credentials.otp_code:
            raise HTTPException(status_code=400, detail="Código OTP requerido")

        totp = pyotp.TOTP(user.otp_secret)
        if not totp.verify(credentials.otp_code):
            raise HTTPException(status_code=401, detail="Código OTP incorrecto")

    # ✅ Aquí se incluye el token
    token = create_access_token({"sub": user.email})
    return {"success": True, "access_token": token}



@router.post("/verify-otp/{user_id}")
def verify_otp(user_id: int, otp_code: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(UserOracle).filter(UserOracle.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    totp = pyotp.TOTP(user.otp_secret)
    if totp.verify(otp_code):
        user.is_2fa_enabled = True
        db.commit()
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Código OTP incorrecto")
