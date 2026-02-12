from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from app.logger import setup_logger
from app.api.chat_routes import router as chat_router


logger = setup_logger()

app = FastAPI(
    title="Saral Pension",
    description="AI-powered pension assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)






@app.get("/")
def root():
    return FileResponse("static/login.html")

@app.get("/login")
def login_page():
    return RedirectResponse("/")

@app.get("/chat")
def chat_page():
    return FileResponse("static/index.html")

@app.get("/health")
def health_check():
    return {"status": "ok"}
