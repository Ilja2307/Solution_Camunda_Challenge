from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Literal
from app import models, database
from app.fetcher import fetch_image_by_type

# ------------------------------------------
# API ROUTER CONFIGURATION
# ------------------------------------------
# This file defines the REST API endpoints
# used to fetch and retrieve animal images.
# All endpoints are grouped using FastAPI's APIRouter
# ------------------------------------------

# Create a router object to register all endpoints in this module
router = APIRouter()


# ------------------------------------------
# SCHEMA for incoming POST request (used in /fetch)
# ------------------------------------------
# This defines the expected structure of the request body
# when calling /fetch. It ensures type safety and validation.
class FetchRequest(BaseModel):
    animal_type: Literal["cat", "dog", "bear"]  # Only accept one of these values
    amount: int = 1  # number of images to fetch (default = 1)


# ------------------------------------------
# Database dependency for FastAPI routes
# ------------------------------------------
# This function opens a new SQLAlchemy session for each request
# and ensures it is properly closed after use.
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------------------
# POST /fetch
# Fetches images from external API and stores them in the DB
# ------------------------------------------
@router.post("/fetch")
async def fetch_images(request: FetchRequest, db: Session = Depends(get_db)):
    # Make sure the requested amount is valid
    if request.amount < 1:
        raise HTTPException(status_code=400, detail="Amount must be at least 1")

    results = []

    # Fetch the number of images requested
    for _ in range(request.amount):
        # Call utility function to fetch image based on type
        image_url = await fetch_image_by_type(request.animal_type)

        # Create a new database record using the returned image URL
        record = models.AnimalImage(
            animal_type=request.animal_type,
            image_url=image_url
        )

        # Save the record to the database
        db.add(record)
        db.commit()
        db.refresh(record)  # Load auto-generated fields like ID and timestamp

        # Print to console for confirmation (useful in Docker logs)
        print(f"Saved image for {record.animal_type}: {record.image_url}")

        # Prepare response data to return to the client
        results.append({
            "id": record.id,
            "animal_type": record.animal_type,
            "image_url": record.image_url,
            "created_at": record.created_at.isoformat()
        })

    return results  # Return the list of saved images


# ------------------------------------------
# GET /last/{animal_type}
# Retrieves the most recently saved image of the given type
# ------------------------------------------
@router.get("/last/{animal_type}")
def get_last_image(
    animal_type: Literal["cat", "dog", "bear"] = Path(..., description="Animal type"),
    db: Session = Depends(get_db)
):
    # Query the database for the latest image matching the type
    record = (
        db.query(models.AnimalImage)
        .filter(models.AnimalImage.animal_type == animal_type)
        .order_by(models.AnimalImage.created_at.desc())  # Order newest → oldest
        .first()
    )

    # Return 404 if no matching image was found 
    if not record:
        raise HTTPException(status_code=404, detail="No image found for this animal type")

    # Return the most recent image record as JSON
    return {
        "id": record.id,
        "animal_type": record.animal_type,
        "image_url": record.image_url,
        "created_at": record.created_at.isoformat()
    }