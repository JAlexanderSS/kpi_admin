# app/api/v1/kpis.py

from fastapi import APIRouter, Depends
from app.db.oracle import get_oracle_users_count
from app.db.sqlserver_utils import get_sqlserver_users_count
from app.db.postgresql import get_postgresql_users_count
from app.auth.jwt_bearer import JWTBearer  # ⬅️ Importar middleware de autenticación

router = APIRouter()

@router.get("/users-distribution", dependencies=[Depends(JWTBearer())])
def get_users_distribution():
    return {
        "Oracle": get_oracle_users_count(),
        "SQL Server": get_sqlserver_users_count(),
        "PostgreSQL": get_postgresql_users_count()
    }
