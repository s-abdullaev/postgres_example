"""CRUD endpoints for course."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Course as CourseModel
from ..schemas import Course, CourseCreate, CourseUpdate

router = APIRouter(prefix="/courses", tags=["course"])


@router.get("", response_model=list[Course])
def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(CourseModel).offset(skip).limit(limit).all()


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: str, db: Session = Depends(get_db)):
    obj = db.query(CourseModel).filter(CourseModel.course_id == course_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Course not found")
    return obj


@router.post("", response_model=Course, status_code=201)
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    obj = CourseModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{course_id}", response_model=Course)
def update_course(course_id: str, data: CourseUpdate, db: Session = Depends(get_db)):
    obj = db.query(CourseModel).filter(CourseModel.course_id == course_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Course not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{course_id}", status_code=204)
def delete_course(course_id: str, db: Session = Depends(get_db)):
    obj = db.query(CourseModel).filter(CourseModel.course_id == course_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(obj)
    db.commit()
    return None
