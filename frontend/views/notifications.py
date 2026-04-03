import streamlit as st

from state.permissions import can_perform_action


def render_notifications_view(role: str | None) -> None:
    st.header("Notifications")

    can_view = can_perform_action(role, "view_notifications")
    st.subheader("Role Permissions")
    st.write(f"View notifications: {'✅' if can_view else '❌'}")

    if not can_view:
        st.error("Your role cannot access notifications.")
        return

    st.divider()
    st.warning("Notifications API integration is planned for issue #9.")
