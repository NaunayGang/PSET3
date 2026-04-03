# OpsCenter

OpsCenter is an incident management platform for the USFQ System Design project.

## Environment setup

Use the root [`.env.example`](.env.example) as the base template for local development.

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
