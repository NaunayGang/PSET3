import streamlit as st

from state.permissions import can_perform_action


def render_tasks_view(role: str | None) -> None:
    st.header("Tasks")

    can_create_task = can_perform_action(role, "create_task")
    can_update_task = can_perform_action(role, "update_task")

    st.subheader("Role Permissions")
    st.write(f"Create tasks: {'✅' if can_create_task else '❌'}")
    st.write(f"Update tasks: {'✅' if can_update_task else '❌'}")

    st.divider()
    st.subheader("Tasks Workspace")
    st.warning("Task management API integration is planned for issue #9.")
