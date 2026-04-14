import streamlit as st

from api_client.client import APIClientError
from forms.task_form import render_task_form
from state.permissions import can_perform_action

TASK_STATUS_OPTIONS = ["OPEN", "IN_PROGRESS", "DONE"]
NEXT_STATUS_BY_CURRENT = {
    "OPEN": ["OPEN", "IN_PROGRESS"],
    "IN_PROGRESS": ["IN_PROGRESS", "DONE"],
    "DONE": ["DONE"],
}


def _format_datetime(value: str | None) -> str:
    if not value:
        return "N/A"
    return value.replace("T", " ").split(".")[0]


def render_tasks_view(role: str | None) -> None:
    st.header("Tasks")

    can_create_task = can_perform_action(role, "create_task")
    can_assign_task = can_perform_action(role, "assign_task")
    can_update_task = can_perform_action(role, "update_task")

    api_client = st.session_state.get("api_client")
    if api_client is None:
        st.error("API client is unavailable. Check API_BASE_URL and try again.")
        return

    controls_col, _ = st.columns([1, 4])
    with controls_col:
        if st.button("Refresh tasks"):
            st.rerun()

    try:
        incidents_response = api_client.get("/incidents")
        incident_options = [incident["id"] for incident in incidents_response] if isinstance(incidents_response, list) else []
    except APIClientError:
        incident_options = []

    if can_create_task:
        task_payload = render_task_form(disabled=False, incident_options=incident_options)
        if task_payload:
            try:
                api_client.post("/tasks", task_payload)
                st.success("Task created successfully.")
                st.rerun()
            except APIClientError as exc:
                st.error(f"Could not create task: {exc}")
    else:
        st.info("Your role cannot create tasks.")

    st.divider()

    try:
        tasks_response = api_client.get("/tasks")
    except APIClientError as exc:
        st.error(f"Could not load tasks: {exc}")
        return

    tasks = tasks_response if isinstance(tasks_response, list) else []
    if not tasks:
        st.info("No tasks available.")
        return

    selected_status_filter = st.selectbox(
        "Filter by status",
        ["ALL", *TASK_STATUS_OPTIONS],
        index=0,
    )

    filtered_tasks = [
        task for task in tasks if selected_status_filter == "ALL" or task.get("status") == selected_status_filter
    ]

    if not filtered_tasks:
        st.info("No tasks match the selected status filter.")
        return

    task_rows = [
        {
            "id": task.get("id"),
            "title": task.get("title"),
            "description": task.get("description"),
            "status": task.get("status"),
            "assigned_to": task.get("assigned_to") or "Unassigned",
            "incident_id": task.get("incident_id"),
            "created_at": _format_datetime(task.get("created_at")),
        }
        for task in filtered_tasks
    ]

    st.subheader("Tasks List")
    st.dataframe(task_rows, use_container_width=True)

    task_options = {f"#{task['id']} - {task['title']}": task for task in filtered_tasks}
    selected_label = st.selectbox("Select task", list(task_options.keys()))
    selected_task = task_options[selected_label]
    selected_task_id = selected_task["id"]

    current_status = selected_task.get("status", "OPEN")
    allowed_statuses = NEXT_STATUS_BY_CURRENT.get(current_status, [current_status])

    action_col_1, action_col_2 = st.columns(2)

    with action_col_1:
        status_value = st.selectbox(
            "Update task status",
            allowed_statuses,
            index=0,
            key=f"task_status_{selected_task_id}",
            disabled=not can_update_task,
        )

        if st.button(
            "Apply task status",
            key=f"apply_task_status_{selected_task_id}",
            disabled=not can_update_task,
        ):
            try:
                api_client.patch(
                    f"/tasks/{selected_task_id}/status",
                    {"status": status_value},
                )
                st.success("Task status updated.")
                st.rerun()
            except APIClientError as exc:
                st.error(f"Could not update task status: {exc}")

    with action_col_2:
        assigned_to_value = st.number_input(
            "Assign to user ID",
            min_value=1,
            step=1,
            value=int(selected_task.get("assigned_to") or 1),
            key=f"task_assign_to_{selected_task_id}",
            disabled=not can_assign_task,
        )

        if st.button(
            "Assign task",
            key=f"assign_task_{selected_task_id}",
            disabled=not can_assign_task,
        ):
            try:
                api_client.patch(
                    f"/tasks/{selected_task_id}",
                    {"assigned_to": int(assigned_to_value)},
                )
                st.success("Task assigned successfully.")
                st.rerun()
            except APIClientError as exc:
                st.error(f"Could not assign task: {exc}")
