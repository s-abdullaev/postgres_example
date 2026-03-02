"""FastAPI application with CRUD endpoints for the university database."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routers import (
    advisor,
    classroom,
    course,
    department,
    instructor,
    prereq,
    section,
    student,
    takes,
    teaches,
    time_slot,
)

app = FastAPI(
    title="University Database API",
    description="""
CRUD API for the university database schema.

## Resources
- **classrooms** – Building/room capacity
- **departments** – Department info and budget
- **courses** – Course catalog
- **instructors** – Faculty
- **students** – Student records
- **sections** – Course sections (semester, year, room)
- **time-slots** – Schedule slots
- **teaches** – Instructor–section assignments
- **takes** – Student enrollments and grades
- **advisors** – Student–instructor advising
- **prereqs** – Course prerequisites
""",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(classroom.router, prefix="/api")
app.include_router(department.router, prefix="/api")
app.include_router(course.router, prefix="/api")
app.include_router(instructor.router, prefix="/api")
app.include_router(student.router, prefix="/api")
app.include_router(section.router, prefix="/api")
app.include_router(time_slot.router, prefix="/api")
app.include_router(teaches.router, prefix="/api")
app.include_router(takes.router, prefix="/api")
app.include_router(advisor.router, prefix="/api")
app.include_router(prereq.router, prefix="/api")


@app.get("/", include_in_schema=False)
def root():
    """Redirect to Swagger UI."""
    return RedirectResponse(url="/docs")
