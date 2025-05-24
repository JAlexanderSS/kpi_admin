from app.db.sqlserver import SessionLocalSqlServer
from app.models.user_sqlserver import UserSQLServer  # Esta importación ya no genera ciclo

def get_sqlserver_users_count():
    db = SessionLocalSqlServer()
    try:
        return db.query(UserSQLServer).count()
    finally:
        db.close()
