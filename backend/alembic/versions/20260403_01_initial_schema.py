"""Initial schema for OpsCenter tables.

Revision ID: 20260403_01
Revises:
Create Date: 2026-04-03
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260403_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "incidents",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("assigned_to", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["assigned_to"], ["users.id"]),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_incidents_id"), "incidents", ["id"], unique=False)
    op.create_index(op.f("ix_incidents_title"), "incidents", ["title"], unique=False)
    op.create_index(op.f("ix_incidents_status"), "incidents", ["status"], unique=False)
    op.create_index(op.f("ix_incidents_created_by"), "incidents", ["created_by"], unique=False)
    op.create_index(op.f("ix_incidents_assigned_to"), "incidents", ["assigned_to"], unique=False)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("incident_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("assigned_to", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["assigned_to"], ["users.id"]),
        sa.ForeignKeyConstraint(["incident_id"], ["incidents.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tasks_id"), "tasks", ["id"], unique=False)
    op.create_index(op.f("ix_tasks_incident_id"), "tasks", ["incident_id"], unique=False)
    op.create_index(op.f("ix_tasks_title"), "tasks", ["title"], unique=False)
    op.create_index(op.f("ix_tasks_status"), "tasks", ["status"], unique=False)
    op.create_index(op.f("ix_tasks_assigned_to"), "tasks", ["assigned_to"], unique=False)

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("recipient_id", sa.Integer(), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["recipient_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notifications_recipient_id"), "notifications", ["recipient_id"], unique=False)
    op.create_index(op.f("ix_notifications_event_type"), "notifications", ["event_type"], unique=False)
    op.create_index(op.f("ix_notifications_status"), "notifications", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_notifications_status"), table_name="notifications")
    op.drop_index(op.f("ix_notifications_event_type"), table_name="notifications")
    op.drop_index(op.f("ix_notifications_recipient_id"), table_name="notifications")
    op.drop_table("notifications")

    op.drop_index(op.f("ix_tasks_assigned_to"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_status"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_title"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_incident_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_id"), table_name="tasks")
    op.drop_table("tasks")

    op.drop_index(op.f("ix_incidents_assigned_to"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_created_by"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_status"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_title"), table_name="incidents")
    op.drop_index(op.f("ix_incidents_id"), table_name="incidents")
    op.drop_table("incidents")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")