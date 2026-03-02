"""Pydantic schemas for request/response validation."""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Classroom
class ClassroomBase(BaseModel):
    building: str
    room_number: str
    capacity: int


class ClassroomCreate(ClassroomBase):
    pass


class ClassroomUpdate(BaseModel):
    capacity: Optional[int] = None


class Classroom(ClassroomBase):
    model_config = ConfigDict(from_attributes=True)


# Department
class DepartmentBase(BaseModel):
    dept_name: str
    building: Optional[str] = None
    budget: Decimal


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    building: Optional[str] = None
    budget: Optional[Decimal] = None


class Department(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)


# Course
class CourseBase(BaseModel):
    course_id: str
    title: Optional[str] = None
    dept_name: Optional[str] = None
    credits: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    dept_name: Optional[str] = None
    credits: Optional[int] = None


class Course(CourseBase):
    model_config = ConfigDict(from_attributes=True)


# Instructor
class InstructorBase(BaseModel):
    id: str
    name: str
    dept_name: Optional[str] = None
    salary: Decimal


class InstructorCreate(InstructorBase):
    pass


class InstructorUpdate(BaseModel):
    name: Optional[str] = None
    dept_name: Optional[str] = None
    salary: Optional[Decimal] = None


class Instructor(InstructorBase):
    model_config = ConfigDict(from_attributes=True)


# Student
class StudentBase(BaseModel):
    id: str
    name: str
    dept_name: Optional[str] = None
    tot_cred: Optional[int] = 0


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    dept_name: Optional[str] = None
    tot_cred: Optional[int] = None


class Student(StudentBase):
    model_config = ConfigDict(from_attributes=True)


# TimeSlot
class TimeSlotBase(BaseModel):
    time_slot_id: str
    day: str
    start_hr: int
    start_min: int
    end_hr: int
    end_min: int


class TimeSlotCreate(TimeSlotBase):
    pass


class TimeSlotUpdate(BaseModel):
    end_hr: Optional[int] = None
    end_min: Optional[int] = None


class TimeSlot(TimeSlotBase):
    model_config = ConfigDict(from_attributes=True)


# Section
class SectionBase(BaseModel):
    course_id: str
    sec_id: str
    semester: str
    year: int
    building: Optional[str] = None
    room_number: Optional[str] = None
    time_slot_id: Optional[str] = None


class SectionCreate(SectionBase):
    pass


class SectionUpdate(BaseModel):
    building: Optional[str] = None
    room_number: Optional[str] = None
    time_slot_id: Optional[str] = None


class Section(SectionBase):
    model_config = ConfigDict(from_attributes=True)


# Teaches
class TeachesBase(BaseModel):
    id: str  # instructor ID
    course_id: str
    sec_id: str
    semester: str
    year: int


class TeachesCreate(TeachesBase):
    pass


class Teaches(TeachesBase):
    model_config = ConfigDict(from_attributes=True)


# Takes
class TakesBase(BaseModel):
    id: str  # student ID
    course_id: str
    sec_id: str
    semester: str
    year: int
    grade: Optional[str] = None


class TakesCreate(TakesBase):
    pass


class TakesUpdate(BaseModel):
    grade: Optional[str] = None


class Takes(TakesBase):
    model_config = ConfigDict(from_attributes=True)


# Advisor
class AdvisorBase(BaseModel):
    s_id: str  # student ID
    i_id: Optional[str] = None  # instructor ID


class AdvisorCreate(AdvisorBase):
    pass


class AdvisorUpdate(BaseModel):
    i_id: Optional[str] = None


class Advisor(AdvisorBase):
    model_config = ConfigDict(from_attributes=True)


# Prereq
class PrereqBase(BaseModel):
    course_id: str
    prereq_id: str


class PrereqCreate(PrereqBase):
    pass


class Prereq(PrereqBase):
    model_config = ConfigDict(from_attributes=True)
