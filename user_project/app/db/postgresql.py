# filepath: c:\Users\josea\Music\uni\administracion\user_project\app\db\postgresql.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os

# Load PostgreSQL connection string from environment variable
postgresql_connection_string = os.getenv("POSTGRESQL_CONNECTION_STRING")

# Create the database engine
engine_pg = create_engine(postgresql_connection_string)
SessionLocalPostgreSQL = sessionmaker(autocommit=False, autoflush=False, bind=engine_pg)