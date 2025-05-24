from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import users, users_oracle, users_sqlserver, kpis, auth  # ⬅️ agrega auth aquí
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

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(users.router, prefix="/api/v1/users", tags=["Usuarios PostgreSQL"])
app.include_router(users_oracle.router, prefix="/api/v1/oracle-users", tags=["Usuarios Oracle"])
app.include_router(users_sqlserver.router, prefix="/api/v1/sql-users", tags=["Usuarios SQL Server"])
app.include_router(kpis.router, prefix="/api/v1/kpis", tags=["KPIs"])
app.include_router(auth.router, prefix="/api/v1", tags=["Autenticación"])  # ⬅️ nueva ruta
