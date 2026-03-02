"""CRUD endpoints for section."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Section as SectionModel
from ..schemas import Section, SectionCreate, SectionUpdate

router = APIRouter(prefix="/sections", tags=["section"])


@router.get("", response_model=list[Section])
def list_sections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(SectionModel).offset(skip).limit(limit).all()


@router.get("/{course_id}/{sec_id}/{semester}/{year}", response_model=Section)
def get_section(
    course_id: str, sec_id: str, semester: str, year: int, db: Session = Depends(get_db)
):
    obj = (
        db.query(SectionModel)
        .filter(
            SectionModel.course_id == course_id,
            SectionModel.sec_id == sec_id,
            SectionModel.semester == semester,
            SectionModel.year == year,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Section not found")
    return obj


@router.post("", response_model=Section, status_code=201)
def create_section(data: SectionCreate, db: Session = Depends(get_db)):
    obj = SectionModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{course_id}/{sec_id}/{semester}/{year}", response_model=Section)
def update_section(
    course_id: str,
    sec_id: str,
    semester: str,
    year: int,
    data: SectionUpdate,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(SectionModel)
        .filter(
            SectionModel.course_id == course_id,
            SectionModel.sec_id == sec_id,
            SectionModel.semester == semester,
            SectionModel.year == year,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Section not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{course_id}/{sec_id}/{semester}/{year}", status_code=204)
def delete_section(
    course_id: str, sec_id: str, semester: str, year: int, db: Session = Depends(get_db)
):
    obj = (
        db.query(SectionModel)
        .filter(
            SectionModel.course_id == course_id,
            SectionModel.sec_id == sec_id,
            SectionModel.semester == semester,
            SectionModel.year == year,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Section not found")
    db.delete(obj)
    db.commit()
    return None
