# OpsCenter API Reference

This document describes the current API surface in the backend implementation, including endpoints, DTO contracts, and authentication/authorization requirements.

## Base information

- Framework: FastAPI
- Base URL (local): `http://localhost:8000`
- Health endpoint: `GET /`
- Auth style: Bearer JWT token
- Token dependency: `OAuth2PasswordBearer(tokenUrl="/auth/login")`

## Authentication and authorization requirements

### Authentication flow

1. Obtain token with `POST /auth/login`.
2. Use the returned token in authenticated requests:

```http
Authorization: Bearer <access_token>
```

### Route-level auth requirements

- Public routes:
  - `GET /`
  - `POST /auth/login`
- Authenticated routes (JWT required):
  - `GET /auth/me`
  - All `/incidents` endpoints
  - All `/tasks` endpoints
  - All `/notifications` endpoints

### Role requirements

Important: route decorators currently do not enforce role dependencies directly (for example, `require_role` aliases are defined but not applied in route signatures). Most restrictions are enforced in use-case logic and data filtering.

Effective behavior today:

- Incident listing:
  - `ADMIN`, `SUPERVISOR`: all incidents.
  - `OPERATOR`: incidents created by or assigned to the operator.
- Task listing:
  - `ADMIN`, `SUPERVISOR`: all tasks (or by incident filter).
  - `OPERATOR`: only assigned tasks.
- Incident assignment:
  - Intended for `ADMIN`/`SUPERVISOR`; current route does not enforce role explicitly.
- Task updates:
  - Assigned user can update own task status/details.
  - `ADMIN`/`SUPERVISOR` can update any task and reassign.
- Notifications:
  - User can list own notifications.
  - User can only update status of own notifications.

## Endpoints

## Root

### GET /

- Description: API health message.
- Auth required: No.
- Response 200:

```json
{
  "message": "OpsCenter API is running"
}
```

## Auth

### POST /auth/login

- Description: Authenticate user and return token.
- Auth required: No.
- Content-Type: `application/x-www-form-urlencoded`
- Request fields:
  - `username` (email value)
  - `password`
- Response 200: `LoginResponse`
- Error 401: invalid credentials.

### GET /auth/me

- Description: Return current authenticated user.
- Auth required: Yes (Bearer token).
- Response 200: `UserResponse`
- Error 401: invalid/expired token.

## Incidents

### GET /incidents

- Description: List incidents with role-based filtering.
- Auth required: Yes.
- Response 200: `IncidentResponse[]`

### GET /incidents/{incident_id}

- Description: Get incident by ID with access check.
- Auth required: Yes.
- Path params:
  - `incident_id: int`
- Response 200: `IncidentResponse`
- Error 404: incident not found or access denied.

### POST /incidents

- Description: Create incident.
- Auth required: Yes.
- Request body: `IncidentCreate`
- Response 200: `IncidentResponse`
- Error 400: validation/business error.

### PATCH /incidents/{incident_id}/assign

- Description: Assign incident to a user.
- Auth required: Yes.
- Path params:
  - `incident_id: int`
- Request body: `IncidentAssign`
- Response 200: `IncidentResponse`
- Error 404: incident/user not found.

### PATCH /incidents/{incident_id}/status

- Description: Change incident status using state-machine validation.
- Auth required: Yes.
- Path params:
  - `incident_id: int`
- Request body: `IncidentStatusUpdate`
- Response 200: `IncidentResponse`
- Error 400: invalid transition or bad input.

## Tasks

### GET /tasks

- Description: List tasks with role-based filtering.
- Auth required: Yes.
- Query params:
  - `incident_id: int` (optional)
- Response 200: `TaskResponse[]`

### POST /tasks

- Description: Create a task linked to an incident.
- Auth required: Yes.
- Request body: `TaskCreate`
- Response 200: `TaskResponse`
- Error 403: insufficient permission.
- Error 404: referenced incident/user not found.

### PATCH /tasks/{task_id}

- Description: Update task fields (title/description/status/assigned_to).
- Auth required: Yes.
- Path params:
  - `task_id: int`
- Request body: `TaskUpdate`
- Response 200: `TaskResponse`
- Error 403: insufficient permission.
- Error 404: task/user not found.

### PATCH /tasks/{task_id}/status

- Description: Convenience endpoint to update only status.
- Auth required: Yes.
- Path params:
  - `task_id: int`
- Request body: `TaskStatusUpdate`
- Response 200: `TaskResponse`
- Error 403: insufficient permission.
- Error 404: task/user not found.

## Notifications

### GET /notifications

- Description: List notifications for current user.
- Auth required: Yes.
- Response 200: `NotificationResponse[]`

### PATCH /notifications/{notification_id}/status

- Description: Update current user's notification status.
- Auth required: Yes.
- Path params:
  - `notification_id: int`
- Request body: `NotificationStatusUpdate`
- Response 200: `NotificationResponse`
- Error 403: notification belongs to another user.
- Error 404: notification not found.

## DTO contracts

## Auth DTOs

### LoginRequest

Note: this DTO exists in application layer. HTTP login route receives OAuth2 form fields (`username`, `password`) and maps them to this DTO.

- `email: EmailStr`
- `password: str`

### LoginResponse

- `access_token: str`
- `token_type: str` (default: `bearer`)
- `user_id: int`
- `name: str`
- `email: str`
- `role: str`

### TokenData

- `user_id: int`
- `email: str`
- `role: str`

## User DTOs

### UserResponse

- `id: int`
- `name: str`
- `email: str`
- `role: str`
- `created_at: datetime`

## Incident DTOs

### IncidentCreate

- `title: str`
- `description: str`
- `severity: IncidentSeverity`

### IncidentUpdate

- `title: str | null`
- `description: str | null`
- `severity: IncidentSeverity | null`

### IncidentAssign

- `assigned_to: int`

### IncidentStatusUpdate

- `status: IncidentStatus`

### IncidentResponse

- `id: int`
- `title: str`
- `description: str`
- `severity: IncidentSeverity`
- `status: IncidentStatus`
- `created_by: int`
- `assigned_to: int | null`
- `created_at: datetime`
- `updated_at: datetime`

## Task DTOs

### TaskCreate

- `incident_id: int`
- `title: str`
- `description: str`

### TaskUpdate

- `title: str | null`
- `description: str | null`
- `status: TaskStatus | null`
- `assigned_to: int | null`

### TaskStatusUpdate

- `status: TaskStatus`

### TaskResponse

- `id: int`
- `incident_id: int`
- `title: str`
- `description: str`
- `status: TaskStatus`
- `assigned_to: int | null`
- `created_at: datetime`
- `updated_at: datetime`

## Notification DTOs

### NotificationStatusUpdate

- `status: NotificationStatus`

### NotificationResponse

- `id: int`
- `recipient_id: int`
- `channel: NotificationChannel`
- `message: str`
- `event_type: EventType`
- `status: NotificationStatus`
- `created_at: datetime`

## Enum values

### Role

- `ADMIN`
- `SUPERVISOR`
- `OPERATOR`

### IncidentSeverity

- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

### IncidentStatus

- `OPEN`
- `ASSIGNED`
- `IN_PROGRESS`
- `RESOLVED`
- `CLOSED`

### TaskStatus

- `OPEN`
- `IN_PROGRESS`
- `DONE`

### NotificationStatus

- `PENDING`
- `SENT`
- `FAILED`

### NotificationChannel

- `EMAIL`
- `SLACK`

### EventType

- `INCIDENT_CREATED`
- `INCIDENT_ASSIGNED`
- `INCIDENT_STATUS_CHANGED`
- `TASK_CREATED`
- `TASK_ASSIGNED`
- `TASK_DONE`

## Example requests

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@opscenter.com&password=password123"
```

### Authenticated incidents list

```bash
curl "http://localhost:8000/incidents" \
  -H "Authorization: Bearer <access_token>"
```

### Create incident

```bash
curl -X POST "http://localhost:8000/incidents" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Payment gateway latency spike",
    "description": "P95 latency exceeded SLA for 12 minutes",
    "severity": "HIGH"
  }'
```
