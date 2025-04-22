from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from app import config

def get_sqlserver_connection_string():
    """Construye la cadena de conexión ODBC para SQL Server."""
    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={config.SQLSERVER_HOST};"
        f"DATABASE={config.SQLSERVER_DB};"
        f"UID={config.SQLSERVER_USER};"
        f"PWD={config.SQLSERVER_PASSWORD};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
    return quote_plus(connection_string)

# Crear la URL completa para SQLAlchemy
DATABASE_URL_SQLSERVER = f"mssql+pyodbc:///?odbc_connect={get_sqlserver_connection_string()}"

# Configurar el motor y la sesión
engine_sqlserver = create_engine(DATABASE_URL_SQLSERVER)
SessionLocalSqlServer = sessionmaker(autocommit=False, autoflush=False, bind=engine_sqlserver)
