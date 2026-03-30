# AGENTS.md - OpsCenter Project Information

## Context & Purpose

**OpsCenter** is an internal platform developed for a **System Design group project at USFQ (Universidad San Francisco de Quito)**. It solves the lack of traceability in a fintech's operational incidents by replacing informal workflows with a robust, integrated management system.

## Architecture: Hexagonal (Ports & Adapters)

We strictly follow a layered isolation approach. No domain code should depend on infrastructure or ORMs.

### 1. Domain (`backend/src/domain`)

- **Entities & Rules:**
    - `User`: id, name, email, role, hashed_password.
    - `Incident`: id, title, description, severity, status, created_by, assigned_to, created_at.
    - `Task`: id, incident_id, title, description, status, assigned_to, created_at.
    - `Notification`: id, recipient, channel, message, event_type, status, created_at.
- **Patterns (Mandatory):**
    - `Observer`: System event management (Publisher/Bus, Observer abstraction, 2+ concrete observers).
    - `Command`: Notification delivery encapsulation (`execute()` method, 2+ concrete commands).
    - `State`: Lifecycle control for `Incident` (OPEN, ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED).
    - `Template Method`: Standardized notification construction across channels (Base class, template method, 2+ implementations).
    - `Factory`: Centralized creation and validation of entities/commands.
- **Repository Interfaces**: Abstract definitions for storage.

### 2. Application (`backend/src/application`)

- **Use Cases**: Login, Create/Assign/Consult Incident, Manage Tasks, Consult Notifications.
- **DTOs**: Pydantic models for API contracts.
- **Flow Coordination**: Connecting domain logic with repository interfaces.

### 3. Infrastructure (`backend/src/infrastructure`)

- **Persistence**: SQLAlchemy models and repository implementations.
- **External Adapters**: Authentication (JWT/Passlib), Notification providers (Email/Slack placeholders).
- **Event Bus**: Concrete implementation for the Observer pattern.

### 4. API Layer (`backend/src/api`)

- FastAPI routes, security guards (JWT), and dependency injection.
- **Endpoints**: `POST /login`, `GET /me`, `GET/POST /incidents`, `PATCH /incidents/{id}/status`, `GET/POST /tasks`, `GET /notifications`.

### 5. Frontend (`frontend/`)

- Streamlit application organized by views, forms, and API clients.
- Views: Login, Incident List, Create Incident Form, Task View, Notifications View.

## Roles & Permissions

- **ADMIN**: Manage users, assign incidents, change all states, view all notifications.
- **SUPERVISOR**: View system/team incidents and tasks, assign incidents, change states.
- **OPERATOR**: Create incidents, view owned/assigned incidents/tasks, update assigned tasks.

## Tech Stack & Workflow

- **Backend**: Python 3.11, FastAPI, SQLAlchemy.
- **Frontend**: Streamlit.
- **Persistence**: PostgreSQL (via Docker).
- **Environment**: Nix Flake (`nix develop`) for deterministic toolsets.
- **GitHub**: All work must map to Issues and PRs with reviews. Use a Project Board (Backlog, Todo, In Progress, In Review, Done).

## Core Requirements (from PSet #3)

1. **Model separation**: Never expose ORM models directly to the API. Use DTOs.
2. **Domain Purity**: Domain layer must have **zero** dependencies on outer layers (FastAPI, SQLAlchemy, etc.).
3. **UML Documentation**: Maintain diagrams in `/docs` (Use Case, Class, Sequence).
4. **Validation**: Factory pattern must centralize input validation.
5. **Incidents Lifecycle**: Must follow the modeled state machine.
6. **Task Flow**: Linked to incidents; states: OPEN, IN_PROGRESS, DONE.
7. **System Events**: Automated notifications on `INCIDENT_CREATED`, `INCIDENT_ASSIGNED`, etc.
8. **Sequence Diagram Flow**: Operator creates incident → Backend persists → Event published → Observer reacts → Notification generated via Template Method → Sent via Command.

## Directory structure

```text
pset3/
├── backend/src/
│   ├── domain/         # Entities, Enums, Patterns, Interfaces
│   ├── application/    # Use Cases, DTOs
│   ├── infrastructure/ # ORM, Repos, Adapters
│   └── api/            # FastAPI Endpoints, Guards
├── frontend/           # Streamlit app
├── docs/               # UML Diagrams
└── scripts/            # Database migrations/scripts
```
