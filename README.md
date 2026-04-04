# OpsCenter

OpsCenter is an incident management platform for the USFQ System Design project.

## Environment setup

Use the root `.env.example` as the base template for local development.

1. Copy `.env.example` to `.env` and adjust values.
2. For backend-only local execution, you can also use [backend/.env.example](backend/.env.example).
3. For frontend-only local execution, you can also use [frontend/.env.example](frontend/.env.example).

### Required variables

- `DATABASE_URL`: PostgreSQL connection string used by backend.
- `SECRET_KEY`: JWT signing key.
- `API_BASE_URL`: Base URL used by Streamlit frontend.
- `LOG_LEVEL`: Logging verbosity.
- `CORS_ALLOW_ORIGINS`, `CORS_ALLOW_METHODS`, `CORS_ALLOW_HEADERS`, `CORS_ALLOW_CREDENTIALS`.

## Environment variable loading

- Backend uses `pydantic-settings` plus `python-dotenv` to load values from `.env`.
- Frontend client uses `python-dotenv` to load `API_BASE_URL`.

## Dockerfiles

- API image: [backend/Dockerfile](backend/Dockerfile)
- UI image: [frontend/Dockerfile](frontend/Dockerfile)

Build examples:

```bash
docker build -t opscenter-api ./backend
docker build -t opscenter-ui ./frontend
```

## Docker Compose setup

This repository includes a full Docker Compose stack with three services:

- db: PostgreSQL 15 with persistent volume
- api: FastAPI backend
- ui: Streamlit frontend

### Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin)

### Environment configuration

1. Copy [.env.example](.env.example) to .env.
2. Adjust values only if needed.

### Run all services

```bash
docker compose up --build
```

### Service endpoints

- API: http://localhost:8000
- UI: http://localhost:8501
- Postgres: localhost:5432

### Health checks

- db: pg_isready
- api: GET /
- ui: GET /_stcore/health

### Stop services

```bash
docker compose down
```

### Remove all data volumes

```bash
docker compose down -v
```

## Database migrations and seed

This project uses Alembic for schema migrations.

### Backend setup

```bash
cd backend
pip install -r requirements.txt
```

### Configure database connection

Set `DATABASE_URL` in your environment or in `backend/.env`.

Example:

```bash
DATABASE_URL=postgresql://opscenter:opscenter@localhost:5432/opscenter
```

### Run migrations

```bash
cd backend
python scripts/migrate.py
```

Equivalent Alembic command:

```bash
cd backend
alembic upgrade head
```

### Seed required test users

```bash
cd backend
python scripts/seed_data.py
```

Users seeded (password: `password123`):

- `admin@opscenter.com` (ADMIN)
- `supervisor@opscenter.com` (SUPERVISOR)
- `operator@opscenter.com` (OPERATOR)

### One-step bootstrap (migrate + seed)

```bash
cd backend
python scripts/bootstrap_db.py
```
