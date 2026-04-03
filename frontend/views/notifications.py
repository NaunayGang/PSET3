import streamlit as st

from api_client.client import APIClientError
from state.permissions import can_perform_action

NOTIFICATION_STATUS_OPTIONS = ["PENDING", "SENT", "FAILED"]
READ_STATUS = "SENT"


def _format_datetime(value: str | None) -> str:
    if not value:
        return "N/A"
    return value.replace("T", " ").split(".")[0]


def render_notifications_view(role: str | None) -> None:
    st.header("Notifications")

    can_view = can_perform_action(role, "view_notifications")
    if not can_view:
        st.error("Your role cannot access notifications.")
        return

    api_client = st.session_state.get("api_client")
    if api_client is None:
        st.error("API client is unavailable. Check API_BASE_URL and try again.")
        return

    controls_col, _ = st.columns([1, 4])
    with controls_col:
        if st.button("Refresh notifications"):
            st.rerun()

    try:
        notifications_response = api_client.get("/notifications")
    except APIClientError as exc:
        st.error(f"Could not load notifications: {exc}")
        return

    notifications = notifications_response if isinstance(notifications_response, list) else []
    if not notifications:
        st.info("No notifications available.")
        return

    event_types = sorted({notification.get("event_type") for notification in notifications if notification.get("event_type")})
    selected_event_filter = st.selectbox("Filter by event type", ["ALL", *event_types], index=0)

    filtered_notifications = [
        notification
        for notification in notifications
        if selected_event_filter == "ALL" or notification.get("event_type") == selected_event_filter
    ]

    if not filtered_notifications:
        st.info("No notifications match the selected event type.")
        return

    notification_rows = [
        {
            "id": notification.get("id"),
            "message": notification.get("message"),
            "event_type": notification.get("event_type"),
            "channel": notification.get("channel"),
            "status": notification.get("status"),
            "created_at": _format_datetime(notification.get("created_at")),
        }
        for notification in filtered_notifications
    ]

    st.subheader("Notifications List")
    st.dataframe(notification_rows, use_container_width=True)

    notification_options = {
        f"#{notification['id']} - {notification['event_type']}": notification
        for notification in filtered_notifications
    }
    selected_label = st.selectbox("Select notification", list(notification_options.keys()))
    selected_notification = notification_options[selected_label]
    selected_notification_id = selected_notification["id"]

    status_value = st.selectbox(
        "Mark notification status",
        NOTIFICATION_STATUS_OPTIONS,
        index=NOTIFICATION_STATUS_OPTIONS.index(selected_notification.get("status", "PENDING")),
        key=f"notification_status_{selected_notification_id}",
    )

    action_col_1, action_col_2 = st.columns(2)

    with action_col_1:
        if st.button("Apply notification status", key=f"apply_notification_status_{selected_notification_id}"):
            try:
                api_client.patch(
                    f"/notifications/{selected_notification_id}/status",
                    {"status": status_value},
                )
                st.success("Notification status updated.")
                st.rerun()
            except APIClientError as exc:
                st.error(f"Could not update notification status: {exc}")

    with action_col_2:
        if st.button("Mark as read", key=f"mark_read_{selected_notification_id}"):
            try:
                api_client.patch(
                    f"/notifications/{selected_notification_id}/status",
                    {"status": READ_STATUS},
                )
                st.success("Notification marked as read.")
                st.rerun()
            except APIClientError as exc:
                st.error(f"Could not mark notification as read: {exc}")
