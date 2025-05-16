from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import users, users_oracle, users_sqlserver
from app.db.base import Base
from app.db.postgresql import engine_pg

# Crear tablas si no existen en PostgreSQL
Base.metadata.create_all(bind=engine_pg)

# Inicializar la app
app = FastAPI(
    title="User Management API",
    version="1.0.0",
    description="API para gestionar usuarios en bases de datos PostgreSQL, Oracle y SQL Server"
)

# Agregar configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En desarrollo, permite todo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas agrupadas por versión de API
app.include_router(users.router, prefix="/api/v1/users", tags=["Usuarios"])
app.include_router(users_oracle.router, prefix="/api/v1/oracle-users", tags=["Oracle Users"])
app.include_router(users_sqlserver.router, prefix="/api/v1/sql-users", tags=["SQL Server Users"])
