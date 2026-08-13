import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Read database URL from environment; fallback to a local SQLite file for
# development if not provided. This prevents startup failures when
# DATABASE_URL is not set in the environment.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Warning: DATABASE_URL not set; falling back to SQLite './dev.db'.")
    DATABASE_URL = "sqlite:///./dev.db"

# Provide SQLite-specific connect args when appropriate.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("Database connected successfully!")
    except Exception as e:
        print("Database connection failed:", e)
