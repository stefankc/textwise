import tracemalloc
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .config import FRONTEND_DIR  # Import the variables
from .routers import files, notes, auth, openai

# Start tracemalloc for more detailed error messages
tracemalloc.start()

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:3000",  # Development frontend
    # "http://localhost:8000",  # Production frontend
    "*"  # Temporarily allow all origins while debugging
]

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(openai.router, prefix="/openai", tags=["openai"])


@app.get("/")
def read_root():
    """
    Root endpoint returning a message.

    Returns:
        dict: A message indicating the service.
    """
    return {"message": "API Key Settings Service"}


# Mount the frontend build directory AFTER defining API routes to prevent route conflicts
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
