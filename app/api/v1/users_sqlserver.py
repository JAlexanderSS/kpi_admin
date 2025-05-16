from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.models.user_sqlserver import UserSQLServer
from app.db.sqlserver import SessionLocalSqlServer as SessionLocalSQL
from app.schemas.user import LoginInput

router = APIRouter()

def get_db():
    db = SessionLocalSQL()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOut)
def create_user_sql(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserSQLServer).filter(UserSQLServer.username == user.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe en SQL Server")
    new_user = UserSQLServer(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserOut])
def get_users_sql(db: Session = Depends(get_db)):
    return db.query(UserSQLServer).all()

@router.get("/{user_id}", response_model=UserOut)
def get_user_sql(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserSQLServer).filter(UserSQLServer.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user_sql(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserSQLServer).filter(UserSQLServer.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=dict)
def delete_user_sql(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserSQLServer).filter(UserSQLServer.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message": f"Usuario con ID {user_id} eliminado correctamente"}

@router.post("/validate-login")
def validate_login(credentials: LoginInput, db: Session = Depends(get_db)):
    user = db.query(UserSQLServer).filter(UserSQLServer.email == credentials.email).first()
    if user and user.password_hash == credentials.password:
        return {"success": True}
    return {"success": False}
