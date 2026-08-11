from sqlmodel import Field, SQLModel, create_engine, Session
from fastapi import Depends
from typing import Annotated
from enum import Enum
from pathlib import Path
sql_file = Path(__file__).parent / "database.db"
sqlite_url = f"sqlite:///{sql_file}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class UserBase(SQLModel):
    username: str = Field(max_length=50, unique=True)
    name: str = Field(max_length=100, unique=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=500)

class UserCreate(UserBase):
    password: str = Field(max_length=100)

class ProjectStatus(str, Enum):
    IN_PROGRESS = "In Progress"
    PLANNING = "Planning"
    ON_HOLD = "On Hold"
    COMPLETED = "Completed"

class ProjectPriority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class ProjectBase(SQLModel):
    client_name: str = Field(max_length=100)
    project_name: str = Field(max_length=100)
    description: str = Field( max_length=500)
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING)
    priority: ProjectPriority = Field(default=ProjectPriority.MEDIUM)
    start_date: str = Field(max_length=10)
    end_date: str = Field(max_length=10)

class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ProjectCreate(ProjectBase):
    pass


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]