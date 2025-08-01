from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------
# DATABASE CONFIGURATION
# ---------------------------

# This app uses a local SQLite database file called "animal_images.db".
# SQLite is perfect for lightweight MVPs because it doesn't require a server setup.
DATABASE_URL = "sqlite:///./animal_images.db"

# Create the SQLAlchemy engine.
# "check_same_thread=False" is required when using SQLite with FastAPI (multi-threaded).
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory to create new database sessions.
# These sessions are used in API routes to read/write data.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base is the superclass for all ORM models.
# All database tables will be defined as subclasses of this Base.
Base = declarative_base()