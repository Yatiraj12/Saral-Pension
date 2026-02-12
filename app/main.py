import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from app.logger import setup_logger
from app.api.chat_routes import router as chat_router


# Setup logger
logger = setup_logger()

# Create FastAPI app
app = FastAPI(
    title="Saral Pension",
    description="AI-powered pension assistant",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(chat_router, prefix="/api")

# Resolve absolute path for static directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# Routes

@app.get("/")
def root():
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))


@app.get("/login")
def login_page():
    return RedirectResponse("/")


@app.get("/chat")
def chat_page():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/health")
def health_check():
    return {"status": "ok"}
