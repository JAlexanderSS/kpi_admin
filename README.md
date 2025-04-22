# 📊 Sistema de Registro de Usuarios y Gestión de KPIs

Este proyecto consiste en una aplicación web con autenticación (login/registro) y funcionalidades para el manejo de KPIs. Utiliza tres bases de datos diferentes y registra la información de usuarios en todas ellas de forma sincronizada. Está orientado al aprendizaje y práctica del uso de servicios en la nube gratuitos, integración de frontend y backend, y uso de múltiples motores de base de datos.

---

## 🚀 Tecnologías utilizadas

### Frontend

- **React JS**
  - Framework moderno para la construcción de interfaces de usuario dinámicas.
  - Componentes reutilizables y manejo eficiente del estado de la aplicación.

### Backend

- **Python con FastAPI**
  - Framework rápido y eficiente para crear APIs REST.
  - Soporte para documentación automática (Swagger UI).
  - Ideal para conectar múltiples bases de datos de forma paralela.

### Gestión de versiones

- **Git**: Control de versiones para mantener un historial de cambios ordenado.
- **GitHub**: Plataforma para alojar el código del proyecto, colaborar y desplegar automáticamente si se desea.

---

## Bases de datos a utilizar

El sistema registra la información del usuario de forma **simultánea** en tres tipos de bases de datos:

- **Oracle**
- **PostgreSQL**
- **MySQL**

Estas bases están alojadas en servicios de nube gratuitos (ver más abajo), y se accede a ellas desde el backend mediante conectores específicos.

---

## Servicios de nube con planes gratuitos

### 🔹 Azure for Students

- Ofrece $100 USD en créditos por 12 meses.
- Incluye servicios como Azure SQL, VMs, App Services y más.
- Requiere cuenta educativa (.edu o similar).

### 🔹 Heroku

- Plan gratuito con contenedores tipo “dyno” para desplegar aplicaciones backend y frontend.
- Permite integraciones con bases de datos (Heroku Postgres).
- Requiere verificación con tarjeta de crédito para algunas funciones.

### 🔹 Google Cloud (Free Tier)

- Incluye una base de datos MySQL y PostgreSQL gratuitas por tiempo limitado (y 90 días de créditos).
- Ideal para alojar APIs en App Engine o Cloud Run.
- Requiere registro con tarjeta.

---

## Estructura de la base de datos

Para mantener un diseño más ordenado y escalable, se han separado las tablas en tres niveles:

### Tabla 1: `login`

| Campo      | Tipo de dato | Descripción                    |
| ---------- | ------------ | ------------------------------ |
| id         | INT / SERIAL | Identificador único (PK)       |
| correo     | VARCHAR(255) | Correo electrónico del usuario |
| contraseña | VARCHAR(255) | Contraseña encriptada          |

---

### 🛠 Scripts base para crear las tablas

#### PostgreSQL (idéntico para MySQL con pequeños ajustes)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    otp_secret TEXT,
    is_2fa_enabled BOOLEAN DEFAULT FALSE
);
```

#### Sql Server

```sql
USE user_db_sql;
GO

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    otp_secret TEXT,
    is_2fa_enabled BIT DEFAULT 0
);
```

#### PostgreSQL

```sql
-- Ya como user_db_oracle
CREATE TABLE users (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR2(100) UNIQUE NOT NULL,
    password_hash CLOB NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR2(10),
    otp_secret CLOB,
    is_2fa_enabled CHAR(1) DEFAULT '0' CHECK (is_2fa_enabled IN ('0', '1'))
);
```
