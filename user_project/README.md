# user_project/user_project/README.md

# Proyecto de Conexión a Bases de Datos

Este proyecto contiene configuraciones para conectarse a diferentes bases de datos: Oracle, PostgreSQL y SQL Server. A continuación se detallan las instrucciones para configurar y ejecutar el proyecto.

## Estructura del Proyecto

```
user_project
├── app
│   ├── db
│   │   ├── oracle.py        # Configuración de conexión a Oracle
│   │   ├── postgresql.py    # Configuración de conexión a PostgreSQL
│   │   └── sqlserver.py     # Configuración de conexión a SQL Server
├── .env                     # Archivo para almacenar credenciales de conexión
└── README.md                # Documentación del proyecto
```

## Configuración de Conexiones

### Oracle

Para conectarse a la base de datos Oracle, asegúrese de tener el controlador adecuado instalado y configure las credenciales en el archivo `.env`:

```
ORACLE_CONNECTION_STRING="DRIVER={Oracle Driver};SERVER=your_server;DATABASE=your_db;UID=your_user;PWD=your_password;"
```

### PostgreSQL

Para la conexión a PostgreSQL, utilice la siguiente estructura en el archivo `.env`:

```
POSTGRESQL_CONNECTION_STRING="postgresql://your_user:your_password@your_host/your_db"
```

### SQL Server

La configuración para SQL Server ya está incluida en el archivo `sqlserver.py`. Asegúrese de que las credenciales en el archivo `.env` sean correctas:

```
SQLSERVER_CONNECTION_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=user_db_sql;UID=ss;PWD=gg;Encrypt=no;TrustServerCertificate=yes;"
```

## Ejecución del Proyecto

1. Asegúrese de tener todas las dependencias instaladas.
2. Configure las credenciales en el archivo `.env`.
3. Ejecute el proyecto utilizando el comando correspondiente para su entorno de desarrollo.

## Notas

- Asegúrese de que los controladores de base de datos necesarios estén instalados en su sistema.
- Revise la documentación de cada base de datos para más detalles sobre la configuración y el uso.