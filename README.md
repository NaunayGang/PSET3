# OpsCenter

OpsCenter is an incident and task management platform created for the USFQ System Design project. It replaces informal incident handling (messages and spreadsheets) with a centralized workflow that supports authentication, traceability, assignments, lifecycle management, and notifications.

OpsCenter provides:

- A central incident register with defined severity and status.
- Role-based workflows for ADMIN, SUPERVISOR, and OPERATOR.
- Linked tasks for execution and follow-up.
- Notification records tied to system events.
- An API + UI stack that enforces consistent process.

## Architechture

The project follows a Hexagonal Architecture (Ports and Adapters) with strict separation of concerns.

- Domain layer (`backend/src/domain`):
	- Entities: User, Incident, Task, Notification.
	- Enums and business rules.
	- Repository interfaces (ports).
	- Design patterns (Observer, Command, State, Template Method, Factory).
- Application layer (`backend/src/application`):
	- Use cases that orchestrate business flows.
	- DTOs for request and response contracts.
- Infrastructure layer (`backend/src/infrastructure`):
	- SQLAlchemy models and repository implementations.
	- Auth adapters (JWT, password hashing).
	- Notification senders and event bus implementation.
- API layer (`backend/src/api`):
	- FastAPI routes and dependency injection.
	- Token-based authentication and role checks.
- Frontend (`frontend`):
	- Streamlit app with views for Login, Incidents, Tasks, and Notifications.

Core stack:

- Backend: Python 3.11, FastAPI, SQLAlchemy.
- Frontend: Streamlit.
- Database: PostgreSQL.
- Migrations: Alembic.
- Containerization: Docker and Docker Compose.

## How to run

### Option 1: Docker Compose (recommended)

1. Copy environment file:

```bash
cp .env.example .env
```

2. Start all services:

```bash
docker compose up --build
```

3. Access services:

- API: http://localhost:8000
- Frontend UI: http://localhost:8501
- PostgreSQL: localhost:5432

4. Stop services:

```bash
docker compose down
```

5. Remove volumes (optional reset):

```bash
docker compose down -v
```

## How to use

1. Open the Streamlit UI at http://localhost:8501.
2. Log in with a seeded account:
	 - `admin@opscenter.com`
	 - `supervisor@opscenter.com`
	 - `operator@opscenter.com`
	 - Password for all: `password123`
3. Navigate through modules in the sidebar:
	 - Incidents: list incidents, create new incidents (role dependent), assign incident, change status.
	 - Tasks: create tasks linked to incidents, filter tasks, update task status.
	 - Notifications: list notifications and update notification status.
4. Use API directly (optional):
	 - Authenticate via `POST /auth/login`.
	 - Get current user with `GET /auth/me`.
	 - Manage incidents via `/incidents` routes.
	 - Manage tasks via `/tasks` routes.
	 - Manage notifications via `/notifications` routes.

Role behavior summary:

- ADMIN: full visibility and control.
- SUPERVISOR: manages assignments and status workflows.
- OPERATOR: creates incidents and updates allowed tasks, with restricted visibility.

## Used patterns

1. Observer pattern

- Purpose: react to domain events and trigger side effects.
- Location: event bus and observers under domain/infrastructure event modules.
- Usage: notification observer listens to events such as incident created, assigned, or status changed.

2. Command pattern

- Purpose: encapsulate notification delivery actions behind `execute()`.
- Location: command interface in domain pattern module; concrete commands for email/slack in infrastructure notification adapters.
- Usage: observers create and execute delivery commands.

3. State pattern

- Purpose: enforce valid incident status transitions.
- Location: incident state machine in domain pattern module.
- Usage: incident status change use case validates lifecycle transitions (OPEN -> ASSIGNED -> IN_PROGRESS -> RESOLVED -> CLOSED, with allowed backward moves where modeled).

4. Template Method pattern

- Purpose: standardize how notification messages are constructed.
- Location: base notification builder and concrete builders for incident/task events.
- Usage: observers use builders to generate subject/body/footer consistently per event type.

5. Factory pattern

- Purpose: centralize entity creation and validation.
- Location: domain factory module.
- Usage: use cases create Incident, Task, Notification entities through factory methods to keep construction and validation rules consistent.

## Abstrac Factory pattern

The project uses a factory abstraction for command creation (`CommandFactory`) and entity construction (`EntityFactory`). The justification is:

- Decoupling: application and domain flows depend on abstractions, not concrete senders or raw constructors.
- Consistency: one place controls creation rules and validation for core objects.
- Extensibility: new notification channels or command types can be added without changing use case logic.
- Testability: factories make it easy to inject test doubles/mocks instead of infrastructure dependencies.

In practical terms, the command factory acts as an Abstract Factory-style mechanism for creating families of related command objects (email/slack delivery commands) behind a common interface.