"""Create university schema (DDL).

Revision ID: 001_ddl
Revises:
Create Date: 2025-03-03

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "001_ddl"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all university tables."""
    op.create_table(
        "classroom",
        sa.Column("building", sa.String(15), nullable=False),
        sa.Column("room_number", sa.String(7), nullable=False),
        sa.Column("capacity", sa.Numeric(4, 0), nullable=True),
        sa.PrimaryKeyConstraint("building", "room_number"),
    )
    op.create_table(
        "department",
        sa.Column("dept_name", sa.String(20), nullable=False),
        sa.Column("building", sa.String(15), nullable=True),
        sa.Column("budget", sa.Numeric(12, 2), nullable=True),
        sa.PrimaryKeyConstraint("dept_name"),
        sa.CheckConstraint("budget > 0", name="department_budget_check"),
    )
    op.create_table(
        "course",
        sa.Column("course_id", sa.String(8), nullable=False),
        sa.Column("title", sa.String(50), nullable=True),
        sa.Column("dept_name", sa.String(20), nullable=True),
        sa.Column("credits", sa.Numeric(2, 0), nullable=True),
        sa.PrimaryKeyConstraint("course_id"),
        sa.ForeignKeyConstraint(
            ["dept_name"],
            ["department.dept_name"],
            ondelete="SET NULL",
        ),
        sa.CheckConstraint("credits > 0", name="course_credits_check"),
    )
    op.create_table(
        "instructor",
        sa.Column("id", sa.String(5), nullable=False),
        sa.Column("name", sa.String(20), nullable=False),
        sa.Column("dept_name", sa.String(20), nullable=True),
        sa.Column("salary", sa.Numeric(8, 2), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["dept_name"],
            ["department.dept_name"],
            ondelete="SET NULL",
        ),
        sa.CheckConstraint("salary > 29000", name="instructor_salary_check"),
    )
    op.create_table(
        "time_slot",
        sa.Column("time_slot_id", sa.String(4), nullable=False),
        sa.Column("day", sa.String(1), nullable=False),
        sa.Column("start_hr", sa.Numeric(2), nullable=False),
        sa.Column("start_min", sa.Numeric(2), nullable=False),
        sa.Column("end_hr", sa.Numeric(2), nullable=True),
        sa.Column("end_min", sa.Numeric(2), nullable=True),
        sa.PrimaryKeyConstraint("time_slot_id", "day", "start_hr", "start_min"),
        sa.CheckConstraint(
            "start_hr >= 0 AND start_hr < 24",
            name="time_slot_start_hr_check",
        ),
        sa.CheckConstraint(
            "start_min >= 0 AND start_min < 60",
            name="time_slot_start_min_check",
        ),
        sa.CheckConstraint(
            "end_hr >= 0 AND end_hr < 24",
            name="time_slot_end_hr_check",
        ),
        sa.CheckConstraint(
            "end_min >= 0 AND end_min < 60",
            name="time_slot_end_min_check",
        ),
    )
    op.create_table(
        "section",
        sa.Column("course_id", sa.String(8), nullable=False),
        sa.Column("sec_id", sa.String(8), nullable=False),
        sa.Column("semester", sa.String(6), nullable=False),
        sa.Column("year", sa.Numeric(4, 0), nullable=False),
        sa.Column("building", sa.String(15), nullable=True),
        sa.Column("room_number", sa.String(7), nullable=True),
        sa.Column("time_slot_id", sa.String(4), nullable=True),
        sa.PrimaryKeyConstraint("course_id", "sec_id", "semester", "year"),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.course_id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["building", "room_number"],
            ["classroom.building", "classroom.room_number"],
            ondelete="SET NULL",
        ),
        sa.CheckConstraint(
            "semester IN ('Fall', 'Winter', 'Spring', 'Summer')",
            name="section_semester_check",
        ),
        sa.CheckConstraint(
            "year > 1701 AND year < 2100",
            name="section_year_check",
        ),
    )
    op.create_table(
        "teaches",
        sa.Column("id", sa.String(5), nullable=False),
        sa.Column("course_id", sa.String(8), nullable=False),
        sa.Column("sec_id", sa.String(8), nullable=False),
        sa.Column("semester", sa.String(6), nullable=False),
        sa.Column("year", sa.Numeric(4, 0), nullable=False),
        sa.PrimaryKeyConstraint("id", "course_id", "sec_id", "semester", "year"),
        sa.ForeignKeyConstraint(
            ["course_id", "sec_id", "semester", "year"],
            ["section.course_id", "section.sec_id", "section.semester", "section.year"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["instructor.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_table(
        "student",
        sa.Column("id", sa.String(5), nullable=False),
        sa.Column("name", sa.String(20), nullable=False),
        sa.Column("dept_name", sa.String(20), nullable=True),
        sa.Column("tot_cred", sa.Numeric(3, 0), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["dept_name"],
            ["department.dept_name"],
            ondelete="SET NULL",
        ),
        sa.CheckConstraint("tot_cred >= 0", name="student_tot_cred_check"),
    )
    op.create_table(
        "takes",
        sa.Column("id", sa.String(5), nullable=False),
        sa.Column("course_id", sa.String(8), nullable=False),
        sa.Column("sec_id", sa.String(8), nullable=False),
        sa.Column("semester", sa.String(6), nullable=False),
        sa.Column("year", sa.Numeric(4, 0), nullable=False),
        sa.Column("grade", sa.String(2), nullable=True),
        sa.PrimaryKeyConstraint("id", "course_id", "sec_id", "semester", "year"),
        sa.ForeignKeyConstraint(
            ["course_id", "sec_id", "semester", "year"],
            ["section.course_id", "section.sec_id", "section.semester", "section.year"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["student.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_table(
        "advisor",
        sa.Column("s_id", sa.String(5), nullable=False),
        sa.Column("i_id", sa.String(5), nullable=True),
        sa.PrimaryKeyConstraint("s_id"),
        sa.ForeignKeyConstraint(
            ["i_id"],
            ["instructor.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["s_id"],
            ["student.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_table(
        "prereq",
        sa.Column("course_id", sa.String(8), nullable=False),
        sa.Column("prereq_id", sa.String(8), nullable=False),
        sa.PrimaryKeyConstraint("course_id", "prereq_id"),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.course_id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["prereq_id"],
            ["course.course_id"],
        ),
    )


def downgrade() -> None:
    """Drop all university tables (reverse dependency order)."""
    op.drop_table("prereq")
    op.drop_table("advisor")
    op.drop_table("takes")
    op.drop_table("student")
    op.drop_table("teaches")
    op.drop_table("section")
    op.drop_table("time_slot")
    op.drop_table("instructor")
    op.drop_table("course")
    op.drop_table("department")
    op.drop_table("classroom")
