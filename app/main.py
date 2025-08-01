from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app import api, models, database
from app.fetcher import fetch_image_by_type
from sqlalchemy.orm import Session

# -------------------------------------------------
# FastAPI app instance
# -------------------------------------------------
app = FastAPI()

# Include the API routes defined in app/api.py
app.include_router(api.router)

# Setup Jinja2 template engine for rendering HTML
templates = Jinja2Templates(directory="app/templates")

# -------------------------------------------------
# Health check endpoint
# Useful for monitoring or testing container readiness
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------------------------------
# Root endpoint ("/")
# Serves a simple welcome HTML page for cleaner UI
# -------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


# -------------------------------------------------
# UI - GET
# Displays the form where users can select animal type and number of images for a cleaner UI
# -------------------------------------------------
@app.get("/ui", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------------------------------
# UI - POST
# Handles form submission:
# - Either fetches new images from external API and saves them
# - Or retrieves the last saved image from the database
# -------------------------------------------------
@app.post("/ui", response_class=HTMLResponse)
async def post_form(
    request: Request,
    animal_type: str = Form(...),   # The animal type selected in the form
    amount: int = Form(1),          # Number of images to fetch (default = 1)
    action: str = Form(...)         # Action: "fetch" or "last"
):
    image_urls = []

    if action == "fetch":
        # Create a new database session
        db: Session = database.SessionLocal()
        try:
            for _ in range(amount):
                # Call API and fetch image URL for selected animal
                image_url = await fetch_image_by_type(animal_type)
                image_urls.append(image_url)

                # Save image record to the database
                record = models.AnimalImage(
                    animal_type=animal_type,
                    image_url=image_url
                )
                db.add(record)
                db.commit()
                db.refresh(record)
                print(f"[UI] Saved {animal_type}: {image_url}")  # Log for Docker/debugging
        finally:
            db.close()

    elif action == "last":
        db: Session = database.SessionLocal()
        try:
            # Query the most recently saved image for that animal type
            record = (
                db.query(models.AnimalImage)
                .filter(models.AnimalImage.animal_type == animal_type)
                .order_by(models.AnimalImage.created_at.desc())
                .first()
            )
            if record:
                image_urls = [record.image_url]
                print(f"[UI] Fetched last {animal_type}: {record.image_url}")
        finally:
            db.close()

    # Render the form again, but with result images displayed
    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_urls": image_urls,
        "animal_type": animal_type,
        "action": action
    })