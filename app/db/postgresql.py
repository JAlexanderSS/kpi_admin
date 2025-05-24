from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
from app.models.user import User  # Asegúrate de importar tu modelo correctamente

DATABASE_URL_PG = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine_pg = create_engine(DATABASE_URL_PG)
SessionLocalPg = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_pg
)

# ✅ Función para contar usuarios
def get_postgresql_users_count():
    db = SessionLocalPg()
    try:
        return db.query(User).count()
    finally:
        db.close()
