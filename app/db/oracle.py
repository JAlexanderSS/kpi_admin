from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import config

DATABASE_URL = (
    f"oracle+oracledb://{config.ORACLE_USER}:{config.ORACLE_PASSWORD}"
    f"@{config.ORACLE_HOST}:{config.ORACLE_PORT}/?service_name={config.ORACLE_SERVICE}"
)

engine_oracle = create_engine(DATABASE_URL)

SessionLocalOracle = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_oracle
)
