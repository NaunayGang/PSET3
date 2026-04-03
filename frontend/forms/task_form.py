import streamlit as st


def render_task_form(disabled: bool = False, incident_options: list[int] | None = None) -> dict | None:
    available_incidents = incident_options or []

    st.subheader("Create Task")
    with st.form("task_form"):
        incident_id = st.selectbox(
            "Incident ID",
            available_incidents,
            disabled=disabled or not available_incidents,
        )
        title = st.text_input("Task title", disabled=disabled)
        description = st.text_area("Task description", disabled=disabled)
        submitted = st.form_submit_button("Save Task", disabled=disabled)

    if not submitted:
        return None

    normalized_title = title.strip()
    normalized_description = description.strip()

    if not available_incidents:
        st.error("No incidents available to link this task.")
        return None

    if not normalized_title or not normalized_description:
        st.error("Title and description are required.")
        return None

    return {
        "incident_id": int(incident_id),
        "title": normalized_title,
        "description": normalized_description,
    }
