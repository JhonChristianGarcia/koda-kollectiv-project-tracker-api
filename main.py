from projects.projects import router as projects_router
from auth.auth import router as auth_router, create_initial_admin
from fastapi import FastAPI
from sqlmodel import Session
from database.database import create_db_and_tables, engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        create_initial_admin(session)
    yield

app = FastAPI(lifespan=lifespan, title="Project Tracker API", description="API for Project Tracker App")

@app.get("/", description="Root endpoint for the Project Tracker API")
def root():
    return {"message": "You've reached the Project Tracker API!"}

app.include_router(auth_router)
app.include_router(projects_router)
