"""CRUD endpoints for time_slot."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import TimeSlot as TimeSlotModel
from ..schemas import TimeSlot, TimeSlotCreate, TimeSlotUpdate

router = APIRouter(prefix="/time-slots", tags=["time_slot"])


@router.get("", response_model=list[TimeSlot])
def list_time_slots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TimeSlotModel).offset(skip).limit(limit).all()


@router.get("/{time_slot_id}/{day}/{start_hr}/{start_min}", response_model=TimeSlot)
def get_time_slot(
    time_slot_id: str,
    day: str,
    start_hr: int,
    start_min: int,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(TimeSlotModel)
        .filter(
            TimeSlotModel.time_slot_id == time_slot_id,
            TimeSlotModel.day == day,
            TimeSlotModel.start_hr == start_hr,
            TimeSlotModel.start_min == start_min,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Time slot not found")
    return obj


@router.post("", response_model=TimeSlot, status_code=201)
def create_time_slot(data: TimeSlotCreate, db: Session = Depends(get_db)):
    obj = TimeSlotModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{time_slot_id}/{day}/{start_hr}/{start_min}", response_model=TimeSlot)
def update_time_slot(
    time_slot_id: str,
    day: str,
    start_hr: int,
    start_min: int,
    data: TimeSlotUpdate,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(TimeSlotModel)
        .filter(
            TimeSlotModel.time_slot_id == time_slot_id,
            TimeSlotModel.day == day,
            TimeSlotModel.start_hr == start_hr,
            TimeSlotModel.start_min == start_min,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Time slot not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{time_slot_id}/{day}/{start_hr}/{start_min}", status_code=204)
def delete_time_slot(
    time_slot_id: str,
    day: str,
    start_hr: int,
    start_min: int,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(TimeSlotModel)
        .filter(
            TimeSlotModel.time_slot_id == time_slot_id,
            TimeSlotModel.day == day,
            TimeSlotModel.start_hr == start_hr,
            TimeSlotModel.start_min == start_min,
        )
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Time slot not found")
    db.delete(obj)
    db.commit()
    return None
