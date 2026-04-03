import streamlit as st

from forms.incident_form import render_incident_form
from state.permissions import can_perform_action


def render_incidents_view(role: str | None) -> None:
    st.header("Incidents")

    can_create = can_perform_action(role, "create_incident")
    can_assign = can_perform_action(role, "assign_incident")
    can_change_status = can_perform_action(role, "change_incident_status")

    st.subheader("Role Permissions")
    st.write(f"Create incidents: {'✅' if can_create else '❌'}")
    st.write(f"Assign incidents: {'✅' if can_assign else '❌'}")
    st.write(f"Change incident status: {'✅' if can_change_status else '❌'}")

    if can_create:
        render_incident_form(disabled=False)
    else:
        st.info("Your role cannot create incidents.")
        render_incident_form(disabled=True)

    st.divider()
    st.subheader("Incident List")
    st.warning("Incident list API integration is planned for issue #8.")
