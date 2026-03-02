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

1. Edit `database/sql/DDL.sql` as needed.
2. Re-run the DDL (this will drop and recreate tables):

   ```bash
   psql -h localhost -U admin -d university -f database/sql/DDL.sql
   ```

3. Re-run `database/sql/DML.sql` if you want to reload sample data.

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
├── database/sql/
│   ├── DDL.sql          # Schema definition
│   ├── DML.sql          # Sample data
│   └── examples.sql     # Example queries
├── tests/               # Pytest tests
├── docker-compose.yml   # PostgreSQL container
├── pyproject.toml      # Dependencies & config
└── .env.example        # Environment template
```
