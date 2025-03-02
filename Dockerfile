# Use Python base image for the web UI and dependencies
FROM python:3.9-slim

# Install wget and other dependencies
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the app code
COPY . /app

# Install Python dependencies (FastAPI and Uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for FastAPI
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
