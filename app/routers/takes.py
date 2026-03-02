"""CRUD endpoints for takes (student enrollment)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Takes as TakesModel
from ..schemas import Takes, TakesCreate, TakesUpdate

router = APIRouter(prefix="/takes", tags=["takes"])


@router.get("", response_model=list[Takes])
def list_takes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TakesModel).offset(skip).limit(limit).all()


@router.get("/{student_id}/{course_id}/{sec_id}/{semester}/{year}", response_model=Takes)
def get_takes(
    student_id: str,
    course_id: str,
    sec_id: str,
    semester: str,
    year: int,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(TakesModel)
        .filter(
            TakesModel.id == student_id,
            TakesModel.course_id == course_id,
            TakesModel.sec_id == sec_id,
            TakesModel.semester == semester,
            TakesModel.year == year,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Takes record not found")
    return obj


@router.post("", response_model=Takes, status_code=201)
def create_takes(data: TakesCreate, db: Session = Depends(get_db)):
    obj = TakesModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{student_id}/{course_id}/{sec_id}/{semester}/{year}", response_model=Takes)
def update_takes(
    student_id: str,
    course_id: str,
    sec_id: str,
    semester: str,
    year: int,
    data: TakesUpdate,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(TakesModel)
        .filter(
            TakesModel.id == student_id,
            TakesModel.course_id == course_id,
            TakesModel.sec_id == sec_id,
            TakesModel.semester == semester,
            TakesModel.year == year,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Takes record not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{student_id}/{course_id}/{sec_id}/{semester}/{year}", status_code=204)
def delete_takes(
    student_id: str,
    course_id: str,
    sec_id: str,
    semester: str,
    year: int,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(TakesModel)
        .filter(
            TakesModel.id == student_id,
            TakesModel.course_id == course_id,
            TakesModel.sec_id == sec_id,
            TakesModel.semester == semester,
            TakesModel.year == year,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Takes record not found")
    db.delete(obj)
    db.commit()
    return None
