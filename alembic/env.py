import os
from logging.config import fileConfig
from urllib.parse import quote_plus

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Importar Base y modelos para autogenerate
from src.infrastructure.db.session import Base
from src.infrastructure.db import models

# Configuración base de Alembic
config = context.config
fileConfig(config.config_file_name)

# Leer variables de entorno y codificar usuario/contraseña
DB_USER = quote_plus(os.getenv("POSTGRES_USER", "postgres"))
DB_PASSWORD = quote_plus(os.getenv("POSTGRES_PASSWORD", "postgres"))
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")

# Connection string final
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Sobrescribir valor para Alembic
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Metadata de modelos para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
