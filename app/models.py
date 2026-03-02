"""SQLAlchemy models for the university database schema."""

from sqlalchemy import (
    Column,
    String,
    Numeric,
    ForeignKey,
    ForeignKeyConstraint,
    CheckConstraint,
)
from .database import Base


class Classroom(Base):
    __tablename__ = "classroom"

    building = Column(String(15), primary_key=True)
    room_number = Column(String(7), primary_key=True)
    capacity = Column(Numeric(4, 0))


class Department(Base):
    __tablename__ = "department"

    dept_name = Column(String(20), primary_key=True)
    building = Column(String(15))
    budget = Column(Numeric(12, 2))

    __table_args__ = (CheckConstraint("budget > 0", name="department_budget_check"),)


class Course(Base):
    __tablename__ = "course"

    course_id = Column(String(8), primary_key=True)
    title = Column(String(50))
    dept_name = Column(String(20), ForeignKey("department.dept_name", ondelete="SET NULL"))
    credits = Column(Numeric(2, 0))

    __table_args__ = (CheckConstraint("credits > 0", name="course_credits_check"),)


class Instructor(Base):
    __tablename__ = "instructor"

    id = Column("id", String(5), primary_key=True, quote=False)
    name = Column(String(20), nullable=False)
    dept_name = Column(String(20), ForeignKey("department.dept_name", ondelete="SET NULL"))
    salary = Column(Numeric(8, 2))

    __table_args__ = (CheckConstraint("salary > 29000", name="instructor_salary_check"),)


class TimeSlot(Base):
    __tablename__ = "time_slot"

    time_slot_id = Column(String(4), primary_key=True)
    day = Column(String(1), primary_key=True)
    start_hr = Column(Numeric(2), primary_key=True)
    start_min = Column(Numeric(2), primary_key=True)
    end_hr = Column(Numeric(2))
    end_min = Column(Numeric(2))

    __table_args__ = (
        CheckConstraint("start_hr >= 0 AND start_hr < 24", name="time_slot_start_hr_check"),
        CheckConstraint("start_min >= 0 AND start_min < 60", name="time_slot_start_min_check"),
        CheckConstraint("end_hr >= 0 AND end_hr < 24", name="time_slot_end_hr_check"),
        CheckConstraint("end_min >= 0 AND end_min < 60", name="time_slot_end_min_check"),
    )


class Section(Base):
    __tablename__ = "section"

    course_id = Column(String(8), ForeignKey("course.course_id", ondelete="CASCADE"), primary_key=True)
    sec_id = Column(String(8), primary_key=True)
    semester = Column(String(6), primary_key=True)
    year = Column(Numeric(4, 0), primary_key=True)
    building = Column(String(15))
    room_number = Column(String(7))
    time_slot_id = Column(String(4))

    __table_args__ = (
        CheckConstraint(
            "semester IN ('Fall', 'Winter', 'Spring', 'Summer')",
            name="section_semester_check",
        ),
        CheckConstraint("year > 1701 AND year < 2100", name="section_year_check"),
        ForeignKeyConstraint(
            ["building", "room_number"],
            ["classroom.building", "classroom.room_number"],
            ondelete="SET NULL",
        ),
    )


class Teaches(Base):
    __tablename__ = "teaches"

    id = Column("id", String(5), ForeignKey("instructor.id", ondelete="CASCADE"), primary_key=True, quote=False)
    course_id = Column(String(8), primary_key=True)
    sec_id = Column(String(8), primary_key=True)
    semester = Column(String(6), primary_key=True)
    year = Column(Numeric(4, 0), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["course_id", "sec_id", "semester", "year"],
            ["section.course_id", "section.sec_id", "section.semester", "section.year"],
            ondelete="CASCADE",
        ),
    )


class Student(Base):
    __tablename__ = "student"

    id = Column("id", String(5), primary_key=True, quote=False)
    name = Column(String(20), nullable=False)
    dept_name = Column(String(20), ForeignKey("department.dept_name", ondelete="SET NULL"))
    tot_cred = Column(Numeric(3, 0))

    __table_args__ = (CheckConstraint("tot_cred >= 0", name="student_tot_cred_check"),)


class Takes(Base):
    __tablename__ = "takes"

    id = Column("id", String(5), ForeignKey("student.id", ondelete="CASCADE"), primary_key=True, quote=False)
    course_id = Column(String(8), primary_key=True)
    sec_id = Column(String(8), primary_key=True)
    semester = Column(String(6), primary_key=True)
    year = Column(Numeric(4, 0), primary_key=True)
    grade = Column(String(2))

    __table_args__ = (
        ForeignKeyConstraint(
            ["course_id", "sec_id", "semester", "year"],
            ["section.course_id", "section.sec_id", "section.semester", "section.year"],
            ondelete="CASCADE",
        ),
    )


class Advisor(Base):
    __tablename__ = "advisor"

    s_id = Column("s_id", String(5), ForeignKey("student.id", ondelete="CASCADE"), primary_key=True)
    i_id = Column("i_id", String(5), ForeignKey("instructor.id", ondelete="SET NULL"))

    __table_args__ = ()


class Prereq(Base):
    __tablename__ = "prereq"

    course_id = Column(
        String(8),
        ForeignKey("course.course_id", ondelete="CASCADE"),
        primary_key=True,
    )
    prereq_id = Column(String(8), ForeignKey("course.course_id"), primary_key=True)
