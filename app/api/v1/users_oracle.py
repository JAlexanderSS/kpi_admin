from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.models.user_oracle import UserOracle
from app.db.oracle import SessionLocalOracle
from app.schemas.user import LoginInput

router = APIRouter()

def get_db():
    db = SessionLocalOracle()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOut)
def create_user_oracle(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserOracle).filter(UserOracle.username == user.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe en Oracle")
    new_user = UserOracle(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

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
    if user and user.password_hash == credentials.password:
        return {"success": True}
    return {"success": False}
