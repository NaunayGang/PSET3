import streamlit as st


SEVERITY_OPTIONS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def render_incident_form(disabled: bool = False) -> dict[str, str] | None:
    st.subheader("Create Incident")
    with st.form("create_incident_form"):
        title = st.text_input("Title", disabled=disabled)
        description = st.text_area("Description", disabled=disabled)
        severity = st.selectbox("Severity", SEVERITY_OPTIONS, disabled=disabled)
        submitted = st.form_submit_button("Submit Incident", disabled=disabled)

    if not submitted:
        return None

    normalized_title = title.strip()
    normalized_description = description.strip()

    if not normalized_title or not normalized_description:
        st.error("Title and description are required.")
        return None

    if severity not in SEVERITY_OPTIONS:
        st.error("Invalid severity selected.")
        return None

    return {
        "title": normalized_title,
        "description": normalized_description,
        "severity": severity,
    }
