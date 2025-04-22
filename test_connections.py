from sqlalchemy import text
from app.db.postgresql import SessionLocalPg
from app.db.oracle import SessionLocalOracle
from app.db.sqlserver import SessionLocalSqlServer


def test_pg():
    print("\n🔵 Probando conexión a PostgreSQL...")
    try:
        db = SessionLocalPg()
        result = db.execute(text("SELECT 1"))
        print("✅ PostgreSQL conectado:", result.fetchone())
    except Exception as e:
        print("❌ Error en PostgreSQL:", e)
    finally:
        db.close()


def test_oracle():
    print("\n🟠 Probando conexión a Oracle...")
    try:
        db = SessionLocalOracle()
        result = db.execute(text("SELECT 1 FROM DUAL"))
        print("✅ Oracle conectado:", result.fetchone())
    except Exception as e:
        print("❌ Error en Oracle:", e)
    finally:
        db.close()


def test_sqlserver():
    print("\n🟣 Probando conexión a SQL Server...")
    try:
        db = SessionLocalSqlServer()
        result = db.execute(text("SELECT 1"))
        print("✅ SQL Server conectado:", result.fetchone())
    except Exception as e:
        print("❌ Error en SQL Server:", e)
    finally:
        db.close()


if __name__ == "__main__":
    print("🔧 Iniciando pruebas de conexión a las bases de datos...")
    test_pg()
    test_oracle()
    test_sqlserver()
    print("\n✅ Pruebas finalizadas.")
