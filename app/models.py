from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

# -----------------------------------------------------------
# ORM Model: AnimalImage
# -----------------------------------------------------------
# This class defines the structure of the "animal_images" table
# using SQLAlchemy's ORM (Object-Relational Mapping).
#
# Each instance of this class represents a row in the database.
# FastAPI can later use this model to insert and query image records.
# -----------------------------------------------------------

class AnimalImage(Base):
    # The name of the database table in SQLite
    __tablename__ = "animal_images"

    # Primary key: auto-incrementing integer ID
    id = Column(Integer, primary_key=True, index=True)

    # Type of animal: either "cat", "dog", or "bear"
    animal_type = Column(String, index=True)

    # URL of the fetched image (as returned by the external API)
    image_url = Column(String)

    # Timestamp when this image was saved (defaults to current UTC time)
    created_at = Column(DateTime, default=datetime.utcnow)