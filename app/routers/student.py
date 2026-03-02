"""CRUD endpoints for student."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Student as StudentModel
from ..schemas import Student, StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["student"])


@router.get("", response_model=list[Student])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(StudentModel).offset(skip).limit(limit).all()


@router.get("/{student_id}", response_model=Student)
def get_student(student_id: str, db: Session = Depends(get_db)):
    obj = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj


@router.post("", response_model=Student, status_code=201)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    obj = StudentModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{student_id}", response_model=Student)
def update_student(student_id: str, data: StudentUpdate, db: Session = Depends(get_db)):
    obj = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    obj = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(obj)
    db.commit()
    return None
