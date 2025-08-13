from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}".format(
    POSTGRES_USER=os.getenv('POSTGRES_USER'),
    POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD'),
    POSTGRES_HOST=os.getenv('POSTGRES_HOST'),
    POSTGRES_PORT=os.getenv('POSTGRES_PORT'),
    POSTGRES_DB=os.getenv('POSTGRES_DB')
)

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Crea una nueva sesión de base de datos"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()