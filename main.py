import os

from projects.projects import router as projects_router
from auth.auth import router as auth_router, create_initial_admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from dotenv import load_dotenv
from database.database import create_db_and_tables, engine
from contextlib import asynccontextmanager

load_dotenv()

DEFAULT_ALLOWED_ORIGINS = "http://localhost:5173,http://localhost:3000"
allowed_origins = [
    origin.strip()
    for origin in os.environ.get("ALLOWED_ORIGINS", DEFAULT_ALLOWED_ORIGINS).split(",")
    if origin.strip()
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        create_initial_admin(session)
    yield

app = FastAPI(lifespan=lifespan, title="Project Tracker API", description="API for Project Tracker App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", description="Root endpoint for the Project Tracker API")
def root():
    return {"message": "You've reached the Project Tracker API!"}

app.include_router(auth_router)
app.include_router(projects_router)
