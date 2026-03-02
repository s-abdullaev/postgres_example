"""CRUD endpoints for teaches (instructor-section assignment)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Teaches as TeachesModel
from ..schemas import Teaches, TeachesCreate

router = APIRouter(prefix="/teaches", tags=["teaches"])


@router.get("", response_model=list[Teaches])
def list_teaches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TeachesModel).offset(skip).limit(limit).all()


@router.get("/{instructor_id}/{course_id}/{sec_id}/{semester}/{year}", response_model=Teaches)
def get_teaches(
    instructor_id: str,
    course_id: str,
    sec_id: str,
    semester: str,
    year: int,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(TeachesModel)
        .filter(
            TeachesModel.id == instructor_id,
            TeachesModel.course_id == course_id,
            TeachesModel.sec_id == sec_id,
            TeachesModel.semester == semester,
            TeachesModel.year == year,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Teaches record not found")
    return obj


@router.post("", response_model=Teaches, status_code=201)
def create_teaches(data: TeachesCreate, db: Session = Depends(get_db)):
    obj = TeachesModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{instructor_id}/{course_id}/{sec_id}/{semester}/{year}", status_code=204)
def delete_teaches(
    instructor_id: str,
    course_id: str,
    sec_id: str,
    semester: str,
    year: int,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(TeachesModel)
        .filter(
            TeachesModel.id == instructor_id,
            TeachesModel.course_id == course_id,
            TeachesModel.sec_id == sec_id,
            TeachesModel.semester == semester,
            TeachesModel.year == year,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Teaches record not found")
    db.delete(obj)
    db.commit()
    return None
