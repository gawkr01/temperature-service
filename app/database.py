from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# I have chosen SQLite for simplicity. For a real app, I might use PostgreSQL or MySQL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tempdata.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# I am using a dependency for the database session so FastAPI can handle opening and closing.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
