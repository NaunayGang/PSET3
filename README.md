# OpsCenter

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
