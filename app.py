import os
import subprocess
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request

# Create FastAPI app
app = FastAPI()

# Define the folder to store downloaded sites
DOWNLOAD_DIR = "/app/downloads"

# Create the directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Set up templates and static files (for HTML and CSS)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": None})

@app.post("/clone", response_class=HTMLResponse)
async def clone(request: Request, url: str = Form(...)):
    # Define the file path for the download
    output_dir = os.path.join(DOWNLOAD_DIR, url.replace("https://", "").replace("http://", "").replace("/", "_"))
    
    # Run the wget command to clone the site
    try:
        subprocess.run(['wget', '--mirror', '--convert-links', '--adjust-extension', '--no-parent', '--directory-prefix', output_dir, url], check=True)
        return templates.TemplateResponse("index.html", {"request": request, "message": "Site cloned successfully!"})
    except subprocess.CalledProcessError:
        return templates.TemplateResponse("index.html", {"request": request, "message": "Error cloning the site."})
