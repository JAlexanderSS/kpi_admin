from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.models.user import User
from app.db.postgresql import SessionLocalPg
from app.schemas.user import LoginInput


router = APIRouter()


def get_db():
    db = SessionLocalPg()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.put("/{user_id}", response_model=UserOut)
def update_user_pg(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en PostgreSQL")
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=dict)
def delete_user_pg(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en PostgreSQL")
    
    db.delete(user)
    db.commit()
    return {"message": f"Usuario con ID {user_id} eliminado correctamente"}

@router.post("/validate-login")
def validate_login(credentials: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if user and user.password_hash == credentials.password:
        return {"success": True}
    return {"success": False}
