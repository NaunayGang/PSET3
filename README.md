# OpsCenter

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
