import streamlit as st


def render_incident_form(disabled: bool = False) -> None:
    st.subheader("Create Incident")
    with st.form("create_incident_form"):
        title = st.text_input("Title", disabled=disabled)
        description = st.text_area("Description", disabled=disabled)
        severity = st.selectbox("Severity", ["LOW", "MEDIUM", "HIGH", "CRITICAL"], disabled=disabled)
        submitted = st.form_submit_button("Submit Incident", disabled=disabled)

    if submitted:
        if not title or not description:
            st.error("Title and description are required.")
            return
        st.info("Incident form submitted. API integration comes in issue #8.")
