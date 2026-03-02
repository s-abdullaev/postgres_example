"""CRUD endpoints for instructor."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Instructor as InstructorModel
from ..schemas import Instructor, InstructorCreate, InstructorUpdate

router = APIRouter(prefix="/instructors", tags=["instructor"])


@router.get("", response_model=list[Instructor])
def list_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(InstructorModel).offset(skip).limit(limit).all()


@router.get("/{instructor_id}", response_model=Instructor)
def get_instructor(instructor_id: str, db: Session = Depends(get_db)):
    obj = db.query(InstructorModel).filter(InstructorModel.id == instructor_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return obj


@router.post("", response_model=Instructor, status_code=201)
def create_instructor(data: InstructorCreate, db: Session = Depends(get_db)):
    obj = InstructorModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{instructor_id}", response_model=Instructor)
def update_instructor(
    instructor_id: str, data: InstructorUpdate, db: Session = Depends(get_db)
):
    obj = db.query(InstructorModel).filter(InstructorModel.id == instructor_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Instructor not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{instructor_id}", status_code=204)
def delete_instructor(instructor_id: str, db: Session = Depends(get_db)):
    obj = db.query(InstructorModel).filter(InstructorModel.id == instructor_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Instructor not found")
    db.delete(obj)
    db.commit()
    return None
