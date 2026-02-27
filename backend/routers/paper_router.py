from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Paper, Workspace, User
from auth import get_current_user
from schemas import PaperResponse

router = APIRouter(prefix="/papers", tags=["Papers"])


# ---------------- UPLOAD PAPER ----------------
@router.post("/{workspace_id}", response_model=PaperResponse)
def upload_paper(
    workspace_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Verify workspace ownership
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    # Save metadata to DB
    new_paper = Paper(
        filename=file.filename,
        workspace_id=workspace_id
    )

    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)

    return new_paper


# ---------------- LIST PAPERS IN WORKSPACE ----------------
@router.get("/{workspace_id}", response_model=List[PaperResponse])
def list_papers(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    papers = db.query(Paper).filter(
        Paper.workspace_id == workspace_id
    ).all()

    return papers