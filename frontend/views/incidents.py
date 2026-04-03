import streamlit as st

from api_client.client import APIClientError
from forms.incident_form import render_incident_form
from state.permissions import can_perform_action

STATUS_OPTIONS = ["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"]


def _format_datetime(value: str | None) -> str:
    if not value:
        return "N/A"
    return value.replace("T", " ").split(".")[0]


def _display_incident_details(incident: dict, tasks: list[dict]) -> None:
    st.markdown(f"### Incident #{incident['id']}: {incident['title']}")
    st.write(incident["description"])

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Severity", incident["severity"])
    col_b.metric("Status", incident["status"])
    col_c.metric("Assigned To", incident.get("assigned_to") or "Unassigned")

    st.caption(
        f"Created by {incident['created_by']} on {_format_datetime(incident.get('created_at'))}"
    )

    st.markdown("#### Associated Tasks")
    if not tasks:
        st.info("No tasks associated with this incident.")
        return

    task_rows = [
        {
            "id": task.get("id"),
            "title": task.get("title"),
            "status": task.get("status"),
            "assigned_to": task.get("assigned_to") or "Unassigned",
            "created_at": _format_datetime(task.get("created_at")),
        }
        for task in tasks
    ]
    st.dataframe(task_rows, use_container_width=True)


def render_incidents_view(role: str | None) -> None:
    st.header("Incidents")

    can_create = can_perform_action(role, "create_incident")
    can_assign = can_perform_action(role, "assign_incident")
    can_change_status = can_perform_action(role, "change_incident_status")

    api_client = st.session_state.get("api_client")
    if api_client is None:
        st.error("API client is unavailable. Check API_BASE_URL and try again.")
        return

    controls_col, _ = st.columns([1, 4])
    with controls_col:
        if st.button("Refresh incidents"):
            st.rerun()

    created_payload = None
    if can_create:
        created_payload = render_incident_form(disabled=False)
    else:
        st.info("Your role cannot create incidents.")

    if created_payload:
        try:
            api_client.post("/incidents", created_payload)
            st.success("Incident created successfully.")
            st.rerun()
        except APIClientError as exc:
            st.error(f"Could not create incident: {exc}")

    st.divider()

    try:
        incidents_response = api_client.get("/incidents")
    except APIClientError as exc:
        st.error(f"Could not load incidents: {exc}")
        return

    incidents = incidents_response if isinstance(incidents_response, list) else []
    if not incidents:
        st.info("No incidents available.")
        return

    incident_rows = [
        {
            "id": incident.get("id"),
            "title": incident.get("title"),
            "description": incident.get("description"),
            "severity": incident.get("severity"),
            "status": incident.get("status"),
            "created_by": incident.get("created_by"),
            "assigned_to": incident.get("assigned_to") or "Unassigned",
            "created_at": _format_datetime(incident.get("created_at")),
        }
        for incident in incidents
    ]

    st.subheader("Incident List")
    st.dataframe(incident_rows, use_container_width=True)

    incident_options = {
        f"#{incident['id']} - {incident['title']}": incident for incident in incidents
    }
    selected_label = st.selectbox("Select incident", list(incident_options.keys()))
    selected_incident = incident_options[selected_label]
    selected_incident_id = selected_incident["id"]

    action_col_1, action_col_2 = st.columns(2)

    with action_col_1:
        status_value = st.selectbox(
            "Update status",
            STATUS_OPTIONS,
            index=STATUS_OPTIONS.index(selected_incident.get("status", "OPEN")),
            key=f"status_{selected_incident_id}",
            disabled=not can_change_status,
        )
        if st.button(
            "Apply status",
            key=f"apply_status_{selected_incident_id}",
            disabled=not can_change_status,
        ):
            try:
                api_client.patch(
                    f"/incidents/{selected_incident_id}/status",
                    {"status": status_value},
                )
                st.success("Incident status updated.")
                st.rerun()
            except APIClientError as exc:
                st.error(f"Could not update status: {exc}")

    with action_col_2:
        assigned_to_value = st.number_input(
            "Assign to user ID",
            min_value=1,
            step=1,
            value=int(selected_incident.get("assigned_to") or 1),
            key=f"assign_to_{selected_incident_id}",
            disabled=not can_assign,
        )
        if st.button(
            "Assign incident",
            key=f"assign_incident_{selected_incident_id}",
            disabled=not can_assign,
        ):
            try:
                api_client.patch(
                    f"/incidents/{selected_incident_id}/assign",
                    {"assigned_to": int(assigned_to_value)},
                )
                st.success("Incident assigned successfully.")
                st.rerun()
            except APIClientError as exc:
                st.error(f"Could not assign incident: {exc}")

    incident_details = selected_incident
    incident_tasks: list[dict] = []

    try:
        tasks_response = api_client.get(f"/tasks?incident_id={selected_incident_id}")
        if isinstance(tasks_response, list):
            incident_tasks = tasks_response
    except APIClientError as exc:
        st.warning(f"Could not load tasks for this incident: {exc}")

    st.divider()
    _display_incident_details(incident_details, incident_tasks)
