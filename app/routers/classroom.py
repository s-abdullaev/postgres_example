"""CRUD endpoints for classroom."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Classroom as ClassroomModel
from ..schemas import Classroom, ClassroomCreate, ClassroomUpdate

router = APIRouter(prefix="/classrooms", tags=["classroom"])


@router.get("", response_model=list[Classroom])
def list_classrooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(ClassroomModel).offset(skip).limit(limit).all()


@router.get("/{building}/{room_number}", response_model=Classroom)
def get_classroom(building: str, room_number: str, db: Session = Depends(get_db)):
    obj = db.query(ClassroomModel).filter(
        ClassroomModel.building == building,
        ClassroomModel.room_number == room_number,
    ).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return obj


@router.post("", response_model=Classroom, status_code=201)
def create_classroom(data: ClassroomCreate, db: Session = Depends(get_db)):
    obj = ClassroomModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{building}/{room_number}", response_model=Classroom)
def update_classroom(
    building: str, room_number: str, data: ClassroomUpdate, db: Session = Depends(get_db)
):
    obj = db.query(ClassroomModel).filter(
        ClassroomModel.building == building,
        ClassroomModel.room_number == room_number,
    ).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Classroom not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{building}/{room_number}", status_code=204)
def delete_classroom(building: str, room_number: str, db: Session = Depends(get_db)):
    obj = db.query(ClassroomModel).filter(
        ClassroomModel.building == building,
        ClassroomModel.room_number == room_number,
    ).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db.delete(obj)
    db.commit()
    return None
