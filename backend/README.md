# CampusLoop Backend

FastAPI backend for the CampusLoop college event platform.

## Current status

The initial backend foundation is in place:
- FastAPI application entry point.
- Environment-based settings.
- SQLAlchemy engine and database-session dependency.
- PostgreSQL readiness and application liveness endpoints.
- Health endpoint tests.

Domain models, Alembic migrations, authentication, and product API routes will be added in subsequent implementation slices. A route should not be considered implemented just because it appears in the API specification.

## Requirements

- Python 3.11 or newer.
- Docker Desktop / Docker Engine with Docker Compose.
- Git.

## Local setup (Windows PowerShell)

From the repository root, start PostgreSQL:

```powershell
docker compose up -d db
```

Then enter the backend folder and create the virtual environment:

```powershell
cd backend
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

Open:
- API documentation: http://localhost:8000/docs
- Liveness: http://localhost:8000/health/live
- Readiness: http://localhost:8000/health/ready

The readiness endpoint returns ready only when PostgreSQL can execute a basic query.

## Run tests

From the `backend/` directory:

```powershell
pytest
```

## Environment

Copy `.env.example` to `.env` and adjust values for your local environment. Never commit `.env` or real credentials. The default Compose password is for local development only.

## Project structure

```text
backend/
  app/
    api/
      health.py
    core/
      config.py
    db/
      base.py
      session.py
    main.py
  tests/
    test_health.py
  pyproject.toml
```

## Engineering notes

- PostgreSQL is the source of truth.
- The app uses SQLAlchemy 2.x patterns.
- Database schema changes will be managed with Alembic once the domain models are introduced.
- Product routes will be added under the versioned `/api/v1` prefix.
- Authorization and college-scope checks belong in backend dependencies/services, not only in the frontend.
