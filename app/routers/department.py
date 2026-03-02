"""CRUD endpoints for department."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Department as DepartmentModel
from ..schemas import Department, DepartmentCreate, DepartmentUpdate

router = APIRouter(prefix="/departments", tags=["department"])


@router.get("", response_model=list[Department])
def list_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(DepartmentModel).offset(skip).limit(limit).all()


@router.get("/{dept_name}", response_model=Department)
def get_department(dept_name: str, db: Session = Depends(get_db)):
    obj = db.query(DepartmentModel).filter(DepartmentModel.dept_name == dept_name).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Department not found")
    return obj


@router.post("", response_model=Department, status_code=201)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    obj = DepartmentModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{dept_name}", response_model=Department)
def update_department(dept_name: str, data: DepartmentUpdate, db: Session = Depends(get_db)):
    obj = db.query(DepartmentModel).filter(DepartmentModel.dept_name == dept_name).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Department not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{dept_name}", status_code=204)
def delete_department(dept_name: str, db: Session = Depends(get_db)):
    obj = db.query(DepartmentModel).filter(DepartmentModel.dept_name == dept_name).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(obj)
    db.commit()
    return None
