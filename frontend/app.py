import streamlit as st

from api_client.client import APIClient, APIClientError
from state.permissions import can_access_view
from state.session import clear_authenticated_session, initialize_session_state
from views.incidents import render_incidents_view
from views.login import render_login_view
from views.notifications import render_notifications_view
from views.tasks import render_tasks_view

st.set_page_config(page_title="OpsCenter", layout="wide")

VIEWS = {
    "Incidents": render_incidents_view,
    "Tasks": render_tasks_view,
    "Notifications": render_notifications_view,
}


def render_sidebar() -> None:
    st.sidebar.title("OpsCenter")

    user = st.session_state.user or {}
    st.sidebar.caption(f"User: {user.get('email', 'N/A')}")
    st.sidebar.caption(f"Role: {st.session_state.role or 'N/A'}")

    available_views = [
        view_name
        for view_name in VIEWS
        if can_access_view(st.session_state.role, view_name)
    ]

    if not available_views:
        st.sidebar.error("No views available for your role.")
        return

    current = st.session_state.current_view
    if current not in available_views:
        st.session_state.current_view = available_views[0]

    st.session_state.current_view = st.sidebar.radio(
        "Navigation",
        options=available_views,
        index=available_views.index(st.session_state.current_view),
    )

    if st.sidebar.button("Logout"):
        clear_authenticated_session()
        st.success("Session closed successfully.")
        st.rerun()


def bootstrap_api_client() -> None:
    if "api_client" in st.session_state:
        return

    try:
        st.session_state.api_client = APIClient()
    except APIClientError as exc:
        st.session_state.api_client = None
        st.error(str(exc))


def main() -> None:
    initialize_session_state()
    bootstrap_api_client()

    if not st.session_state.is_authenticated:
        render_login_view()
        return

    render_sidebar()

    selected_view = st.session_state.current_view
    if not can_access_view(st.session_state.role, selected_view):
        st.error("You are not allowed to access this section.")
        return

    renderer = VIEWS[selected_view]
    renderer(st.session_state.role)


if __name__ == "__main__":
    main()
