# University Database API

A FastAPI application providing CRUD endpoints for a university database schema backed by PostgreSQL.

## Prerequisites

- **Python 3.13+**
- **Docker** (for PostgreSQL)
- **uv** (recommended) or pip for dependency management

## Quick Start

### 1. Clone and enter the project

```bash
cd postgres
```

### 2. Start the database

```bash
docker compose up -d
```

This starts PostgreSQL 16 on port 5432 with:
- Database: `university`
- User: `admin`
- Password: `admin123`

### 3. Initialize the database schema

Run the DDL and DML scripts to create tables and seed data:

```bash
# Create tables
psql -h localhost -U admin -d university -f database/sql/DDL.sql

# Load sample data (optional)
psql -h localhost -U admin -d university -f database/sql/DML.sql
```

When prompted, use password: `admin123`.

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` if your database settings differ from the defaults.

### 5. Install dependencies

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```

### 6. Run the application

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- **API docs (Swagger):** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc  

## Running Tests

```bash
uv run pytest
```

Or:

```bash
pytest
```

Run with verbose output:

```bash
uv run pytest -v
```

## Updating the Project

### Update dependencies

```bash
uv sync
```

To add a new dependency:

```bash
uv add <package-name>
```

### Update database schema

**Using Alembic (recommended):** After changing `app/models.py`, create and apply a migration. See [Database Migrations with Alembic](#database-migrations-with-alembic) below.

**Using DDL directly (dev/reset):** For a full schema reset, edit `database/sql/DDL.sql` and run:

```bash
psql -h localhost -U admin -d university -f database/sql/DDL.sql
```

Then re-run `database/sql/DML.sql` to reload sample data.

### Pull latest changes

```bash
git pull
uv sync
```

## API Resources

| Resource    | Description                    |
|------------|--------------------------------|
| classrooms | Building/room capacity        |
| departments| Department info and budget    |
| courses    | Course catalog                |
| instructors| Faculty                       |
| students   | Student records               |
| sections   | Course sections (semester, year, room) |
| time-slots | Schedule slots                |
| teaches    | Instructor–section assignments|
| takes      | Student enrollments and grades|
| advisors   | Student–instructor advising   |
| prereqs    | Course prerequisites          |

## Project Structure

```
postgres/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── database.py      # DB connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── routers/         # API route handlers
├── alembic/
│   ├── env.py           # Migration environment
│   └── versions/        # Migration scripts
├── database/sql/
│   ├── DDL.sql          # Schema definition
│   ├── DML.sql          # Sample data
│   └── examples.sql     # Example queries
├── tests/               # Pytest tests
├── docker-compose.yml   # PostgreSQL container
├── pyproject.toml      # Dependencies & config
└── .env.example        # Environment template
```

---

## Development Guide

### Adding New Models and API Endpoints (SQLAlchemy)

To add a new resource to the API, follow these steps:

#### 1. Define the SQLAlchemy model

Edit `app/models.py` and add a new model class inheriting from `Base`. Match table and column names to your schema:

```python
from sqlalchemy import Column, String, Numeric, ForeignKey

class MyResource(Base):
    __tablename__ = "my_table"

    id = Column(String(5), primary_key=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(String(5), ForeignKey("other_table.id", ondelete="SET NULL"))
```

Use `Column` types: `String(n)`, `Numeric(p,s)`, `Integer`, `Boolean`, `DateTime`, etc. Add `CheckConstraint` or `ForeignKeyConstraint` in `__table_args__` if needed.

#### 2. Define Pydantic schemas

Edit `app/schemas.py` and add request/response schemas. Use `Base`, `Create`, `Update`, and a response schema with `model_config = ConfigDict(from_attributes=True)`:

```python
class MyResourceBase(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None

class MyResourceCreate(MyResourceBase):
    pass

class MyResourceUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[str] = None

class MyResource(MyResourceBase):
    model_config = ConfigDict(from_attributes=True)
```

#### 3. Create the router

Create `app/routers/my_resource.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import MyResource as MyResourceModel
from ..schemas import MyResource, MyResourceCreate, MyResourceUpdate

router = APIRouter(prefix="/my-resources", tags=["my-resource"])

@router.get("", response_model=list[MyResource])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(MyResourceModel).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=MyResource)
def get_item(item_id: str, db: Session = Depends(get_db)):
    obj = db.query(MyResourceModel).filter(MyResourceModel.id == item_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.post("", response_model=MyResource, status_code=201)
def create_item(data: MyResourceCreate, db: Session = Depends(get_db)):
    obj = MyResourceModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.patch("/{item_id}", response_model=MyResource)
def update_item(item_id: str, data: MyResourceUpdate, db: Session = Depends(get_db)):
    obj = db.query(MyResourceModel).filter(MyResourceModel.id == item_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: str, db: Session = Depends(get_db)):
    obj = db.query(MyResourceModel).filter(MyResourceModel.id == item_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(obj)
    db.commit()
    return None
```

For composite primary keys, adjust path params and filters (e.g. `filter(Model.col1 == v1, Model.col2 == v2)`).

#### 4. Register the router

Edit `app/main.py`: add the import and include the router:

```python
from .routers import my_resource
app.include_router(my_resource.router, prefix="/api")
```

---

### Writing Tests with pytest

Tests use `TestClient` with a database session that rolls back after each test (see `tests/conftest.py`), so tests do not persist changes.

#### Test structure

Create `tests/test_my_resource.py`:

```python
"""Tests for my-resource CRUD endpoints."""

def test_list_items(client):
    r = client.get("/api/my-resources")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)

def test_get_item(client):
    # Assume an item exists from seed data, or create one first
    r = client.get("/api/my-resources/some_id")
    assert r.status_code == 200
    assert r.json()["id"] == "some_id"

def test_get_item_not_found(client):
    r = client.get("/api/my-resources/nonexistent")
    assert r.status_code == 404

def test_create_item(client):
    r = client.post(
        "/api/my-resources",
        json={"id": "99999", "name": "Test", "parent_id": None},
    )
    assert r.status_code == 201
    assert r.json()["name"] == "Test"

def test_update_item(client):
    client.post("/api/my-resources", json={"id": "99999", "name": "Test"})
    r = client.patch("/api/my-resources/99999", json={"name": "Updated"})
    assert r.status_code == 200
    assert r.json()["name"] == "Updated"

def test_delete_item(client):
    client.post("/api/my-resources", json={"id": "99999", "name": "Test"})
    r = client.delete("/api/my-resources/99999")
    assert r.status_code == 204
    r2 = client.get("/api/my-resources/99999")
    assert r2.status_code == 404
```

The `client` fixture is provided by `conftest.py` and overrides `get_db` with a rollback session.

#### Running tests

```bash
uv run pytest                    # all tests
uv run pytest tests/test_my_resource.py   # single module
uv run pytest -v                 # verbose
uv run pytest -k "test_create"   # match test names
```

---

### Database Migrations with Alembic

Use Alembic to version database schema changes instead of manually editing DDL.

#### Creating a migration

After changing `app/models.py`, generate a migration:

```bash
uv run alembic revision --autogenerate -m "add my_table"
```

This creates a new file in `alembic/versions/` (e.g. `002_add_my_table.py`). **Review the generated script** — autogenerate may miss constraints, renames, or data migrations.

#### Applying migrations

```bash
uv run alembic upgrade head
```

To migrate one step:

```bash
uv run alembic upgrade +1
```

#### Rolling back

```bash
uv run alembic downgrade -1    # one revision back
uv run alembic downgrade base # all the way back
```

#### Manual migrations

For complex changes, create an empty revision:

```bash
uv run alembic revision -m "add custom index"
```

Then edit the generated file: implement `upgrade()` and `downgrade()` using `op.create_table`, `op.add_column`, `op.drop_column`, etc.:

```python
def upgrade():
    op.create_table(
        "my_table",
        sa.Column("id", sa.String(5), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
    )
    op.create_index("ix_my_table_name", "my_table", ["name"])

def downgrade():
    op.drop_index("ix_my_table_name", table_name="my_table")
    op.drop_table("my_table")
```

#### Migration workflow

1. Change `app/models.py`.
2. Run `alembic revision --autogenerate -m "description"`.
3. Inspect and adjust the migration file.
4. Run `alembic upgrade head` to apply.
