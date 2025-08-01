from app.database import Base, engine
from app import models

# ---------------------------------------
# Database Initialization Script
# ---------------------------------------
# This script is responsible for creating all database tables
# based on the ORM models defined in app/models.py.
# It uses SQLAlchemy's Base metadata to generate the schema.
# 
# This is typically run once before the app is used,
# or included in a startup routine for Docker.
# ---------------------------------------

def init():
    # Create all tables defined via SQLAlchemy ORM models
    # If tables already exist, nothing will be changed
    Base.metadata.create_all(bind=engine)