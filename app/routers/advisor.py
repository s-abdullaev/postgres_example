"""CRUD endpoints for advisor (student-instructor advising)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Advisor as AdvisorModel
from ..schemas import Advisor, AdvisorCreate, AdvisorUpdate

router = APIRouter(prefix="/advisors", tags=["advisor"])


@router.get("", response_model=list[Advisor])
def list_advisors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(AdvisorModel).offset(skip).limit(limit).all()


@router.get("/{student_id}", response_model=Advisor)
def get_advisor(student_id: str, db: Session = Depends(get_db)):
    obj = db.query(AdvisorModel).filter(AdvisorModel.s_id == student_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Advisor not found")
    return obj


@router.post("", response_model=Advisor, status_code=201)
def create_advisor(data: AdvisorCreate, db: Session = Depends(get_db)):
    obj = AdvisorModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{student_id}", response_model=Advisor)
def update_advisor(student_id: str, data: AdvisorUpdate, db: Session = Depends(get_db)):
    obj = db.query(AdvisorModel).filter(AdvisorModel.s_id == student_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Advisor not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{student_id}", status_code=204)
def delete_advisor(student_id: str, db: Session = Depends(get_db)):
    obj = db.query(AdvisorModel).filter(AdvisorModel.s_id == student_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Advisor not found")
    db.delete(obj)
    db.commit()
    return None
