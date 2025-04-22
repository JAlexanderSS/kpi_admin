from fastapi import FastAPI
from app.api.v1 import users
from app.db.base import Base
from app.db.postgresql import engine_pg

# Crear tablas si no existen
Base.metadata.create_all(bind=engine_pg)

app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
