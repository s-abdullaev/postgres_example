"""CRUD endpoints for prereq (course prerequisites)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Prereq as PrereqModel
from ..schemas import Prereq, PrereqCreate

router = APIRouter(prefix="/prereqs", tags=["prereq"])


@router.get("", response_model=list[Prereq])
def list_prereqs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(PrereqModel).offset(skip).limit(limit).all()


@router.get("/{course_id}/{prereq_id}", response_model=Prereq)
def get_prereq(course_id: str, prereq_id: str, db: Session = Depends(get_db)):
    obj = (
        db.query(PrereqModel)
        .filter(
            PrereqModel.course_id == course_id,
            PrereqModel.prereq_id == prereq_id,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Prereq not found")
    return obj


@router.post("", response_model=Prereq, status_code=201)
def create_prereq(data: PrereqCreate, db: Session = Depends(get_db)):
    obj = PrereqModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{course_id}/{prereq_id}", status_code=204)
def delete_prereq(course_id: str, prereq_id: str, db: Session = Depends(get_db)):
    obj = (
        db.query(PrereqModel)
        .filter(
            PrereqModel.course_id == course_id,
            PrereqModel.prereq_id == prereq_id,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Prereq not found")
    db.delete(obj)
    db.commit()
    return None
