# Use official Python 3.12 base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to cache Docker layers
COPY requirements.txt .

# Install Python dependencies inside container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Initialize the SQLite database on container startup and then run the app
CMD ["bash", "-c", "python -c 'from app.init_db import init; init()' && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
