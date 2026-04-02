PERMISSIONS = {
    "ADMIN": {
        "views": {"Incidents", "Tasks", "Notifications"},
        "actions": {
            "create_incident",
            "assign_incident",
            "change_incident_status",
            "create_task",
            "update_task",
            "view_notifications",
        },
    },
    "SUPERVISOR": {
        "views": {"Incidents", "Tasks", "Notifications"},
        "actions": {
            "assign_incident",
            "change_incident_status",
            "create_task",
            "update_task",
            "view_notifications",
        },
    },
    "OPERATOR": {
        "views": {"Incidents", "Tasks", "Notifications"},
        "actions": {
            "create_incident",
            "update_task",
            "view_notifications",
        },
    },
}


def can_access_view(role: str | None, view_name: str) -> bool:
    if role is None:
        return False
    return view_name in PERMISSIONS.get(role, {}).get("views", set())


def can_perform_action(role: str | None, action_name: str) -> bool:
    if role is None:
        return False
    return action_name in PERMISSIONS.get(role, {}).get("actions", set())
