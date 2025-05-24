from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.oracle import SessionLocalOracle
from app.db.postgresql import SessionLocalPg
from app.db.sqlserver import SessionLocalSqlServer
from app.models.user_oracle import UserOracle
from app.models.user import User as UserPostgres
from app.models.user_sqlserver import UserSQLServer
from app.schemas.user import LoginInput
from app.auth.jwt_handler import create_access_token

router = APIRouter()

def get_all_sessions():
    return {
        "oracle": SessionLocalOracle(),
        "postgres": SessionLocalPg(),
        "sqlserver": SessionLocalSqlServer()
    }

@router.post("/login")
def login_user(credentials: LoginInput):
    sessions = get_all_sessions()
    email = credentials.email
    password = credentials.password

    try:
        # Revisar en Oracle
        user = sessions["oracle"].query(UserOracle).filter(UserOracle.email == email).first()
        if user and user.password_hash == password:
            token = create_access_token({"sub": user.email})
            return {"access_token": token}

        # Revisar en PostgreSQL
        user = sessions["postgres"].query(UserPostgres).filter(UserPostgres.email == email).first()
        if user and user.password_hash == password:
            token = create_access_token({"sub": user.email})
            return {"access_token": token}

        # Revisar en SQL Server
        user = sessions["sqlserver"].query(UserSQLServer).filter(UserSQLServer.email == email).first()
        if user and user.password_hash == password:
            token = create_access_token({"sub": user.email})
            return {"access_token": token}

        # Si no se encontró en ninguna
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    finally:
        for db in sessions.values():
            db.close()
