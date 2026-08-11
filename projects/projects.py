from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from auth.auth import get_current_user
from database.database import Project, ProjectCreate, SessionDep
router = APIRouter(prefix="/projects", tags=["Project Management"], dependencies=[Depends(get_current_user)])

@router.get("/")
def get_projects(session: SessionDep):
    projects = session.exec(select(Project)).all()
    return {"projects": projects}

@router.post("/", description="Create a new project")
def create_project(project: ProjectCreate, session: SessionDep):
    db_project = Project(**project.model_dump())
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return {"message": "Project created", "project": db_project}

@router.put("/{project_id}", description="Update a project by ID")
def update_project(project_id: int, data: ProjectCreate, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in data.model_dump().items():
        setattr(project, key, value)
    session.commit()
    session.refresh(project)
    return {"message": "Project updated", "project": project}

@router.delete("/{project_id}", description="Delete a project by ID")
def delete_project(project_id: int, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"message": "Project deleted"}