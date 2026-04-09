"""Tests for NotificationObserver full event handling."""

from datetime import datetime, timezone

from src.domain.entities.incident import Incident
from src.domain.entities.notification import Notification
from src.domain.entities.task import Task
from src.domain.entities.user import User
from src.domain.enums.event_type import EventType
from src.domain.enums.incident_severity import IncidentSeverity
from src.domain.enums.incident_status import IncidentStatus
from src.domain.enums.notification_channel import NotificationChannel
from src.domain.enums.notification_status import NotificationStatus
from src.domain.enums.role import Role
from src.domain.enums.task_status import TaskStatus
from src.domain.patterns.concrete_observers import NotificationObserver
from src.domain.patterns.factory import CommandFactory
from src.domain.patterns.observer import DomainEvent


class InMemoryNotificationRepository:
    def __init__(self):
        self.notifications: dict[int, Notification] = {}
        self._next_id = 1

    def find_by_id(self, notification_id: int):
        return self.notifications.get(notification_id)

    def save(self, notification: Notification) -> Notification:
        if notification.id is None:
            notification.id = self._next_id
            self._next_id += 1
        self.notifications[notification.id] = notification
        return notification

    def list_by_recipient(self, user_id: int):
        return [n for n in self.notifications.values() if n.recipient_id == user_id]

    def list_by_status(self, status: NotificationStatus):
        return [n for n in self.notifications.values() if n.status == status]

    def update_status(self, notification_id: int, status: NotificationStatus):
        notification = self.notifications.get(notification_id)
        if not notification:
            return None
        notification.status = status
        return notification

    def delete(self, notification_id: int) -> bool:
        if notification_id in self.notifications:
            del self.notifications[notification_id]
            return True
        return False


class InMemoryUserRepository:
    def __init__(self, users: list[User]):
        self.users = {u.id: u for u in users}

    def find_by_id(self, user_id: int):
        return self.users.get(user_id)

    def find_by_email(self, email: str):
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def save(self, user: User):
        self.users[user.id] = user
        return user

    def list_all(self):
        return list(self.users.values())

    def delete(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


class InMemoryIncidentRepository:
    def __init__(self, incidents: list[Incident]):
        self.incidents = {i.id: i for i in incidents}

    def find_by_id(self, incident_id: int):
        return self.incidents.get(incident_id)

    def save(self, incident: Incident):
        self.incidents[incident.id] = incident
        return incident

    def list_all(self):
        return list(self.incidents.values())

    def list_by_creator(self, user_id: int):
        return [i for i in self.incidents.values() if i.created_by == user_id]

    def list_by_assignee(self, user_id: int):
        return [i for i in self.incidents.values() if i.assigned_to == user_id]

    def list_by_status(self, status: IncidentStatus):
        return [i for i in self.incidents.values() if i.status == status]

    def update_status(self, incident_id: int, status: IncidentStatus):
        incident = self.incidents.get(incident_id)
        if not incident:
            return None
        incident.status = status
        return incident

    def delete(self, incident_id: int) -> bool:
        if incident_id in self.incidents:
            del self.incidents[incident_id]
            return True
        return False


class InMemoryTaskRepository:
    def __init__(self, tasks: list[Task]):
        self.tasks = {t.id: t for t in tasks}

    def find_by_id(self, task_id: int):
        return self.tasks.get(task_id)

    def save(self, task: Task):
        self.tasks[task.id] = task
        return task

    def list_by_incident(self, incident_id: int):
        return [t for t in self.tasks.values() if t.incident_id == incident_id]

    def list_by_assignee(self, user_id: int):
        return [t for t in self.tasks.values() if t.assigned_to == user_id]

    def list_by_status(self, status: TaskStatus):
        return [t for t in self.tasks.values() if t.status == status]

    def list_all(self):
        return list(self.tasks.values())

    def update_status(self, task_id: int, status: TaskStatus):
        task = self.tasks.get(task_id)
        if not task:
            return None
        task.status = status
        return task

    def delete(self, task_id: int) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False


def _build_test_observer():
    now = datetime.now(timezone.utc)

    users = [
        User(id=1, name="Creator", email="creator@test.com", role=Role.OPERATOR, hashed_password="x", created_at=now),
        User(id=2, name="Assignee", email="assignee@test.com", role=Role.SUPERVISOR, hashed_password="x", created_at=now),
        User(id=3, name="Watcher", email="watcher@test.com", role=Role.ADMIN, hashed_password="x", created_at=now),
    ]

    incidents = [
        Incident(
            id=100,
            title="API Outage",
            description="Service unavailable",
            severity=IncidentSeverity.HIGH,
            status=IncidentStatus.ASSIGNED,
            created_by=1,
            assigned_to=2,
            created_at=now,
            updated_at=now,
        )
    ]

    tasks = [
        Task(
            id=200,
            incident_id=100,
            title="Restart service",
            description="Redeploy backend",
            status=TaskStatus.IN_PROGRESS,
            assigned_to=2,
            created_at=now,
            updated_at=now,
        )
    ]

    observer = NotificationObserver(
        notification_repo=InMemoryNotificationRepository(),
        user_repo=InMemoryUserRepository(users),
        incident_repo=InMemoryIncidentRepository(incidents),
        task_repo=InMemoryTaskRepository(tasks),
        command_factory=CommandFactory(),
    )

    return observer


def test_task_assigned_event_creates_notification_for_assignee():
    observer = _build_test_observer()

    observer.update(
        DomainEvent(
            event_type=EventType.TASK_ASSIGNED,
            data={
                "task_id": 200,
                "assigned_to_id": 2,
                "assigner_id": 3,
            },
            timestamp=datetime.now(timezone.utc),
        )
    )

    notifications = observer.notification_repo.list_by_recipient(2)
    assert len(notifications) == 1
    assert notifications[0].event_type == EventType.TASK_ASSIGNED
    assert notifications[0].status == NotificationStatus.SENT
    assert notifications[0].channel == NotificationChannel.EMAIL


def test_task_done_event_notifies_other_stakeholders():
    observer = _build_test_observer()

    observer.update(
        DomainEvent(
            event_type=EventType.TASK_DONE,
            data={
                "task_id": 200,
                "incident_id": 100,
                "completed_by": 2,
            },
            timestamp=datetime.now(timezone.utc),
        )
    )

    creator_notifications = observer.notification_repo.list_by_recipient(1)
    assignee_notifications = observer.notification_repo.list_by_recipient(2)

    assert len(creator_notifications) == 1
    assert creator_notifications[0].event_type == EventType.TASK_DONE
    assert creator_notifications[0].status == NotificationStatus.SENT

    # Completer should be excluded from recipients for completion event.
    assert len(assignee_notifications) == 0


def test_task_created_event_notifies_incident_stakeholders_except_creator():
    observer = _build_test_observer()

    observer.update(
        DomainEvent(
            event_type=EventType.TASK_CREATED,
            data={
                "task_id": 200,
                "incident_id": 100,
                "creator_id": 1,
            },
            timestamp=datetime.now(timezone.utc),
        )
    )

    creator_notifications = observer.notification_repo.list_by_recipient(1)
    assignee_notifications = observer.notification_repo.list_by_recipient(2)

    assert len(creator_notifications) == 0
    assert len(assignee_notifications) == 1
    assert assignee_notifications[0].event_type == EventType.TASK_CREATED
    assert assignee_notifications[0].status == NotificationStatus.SENT
