import streamlit as st

from api_client.client import APIClientError
from state.session import set_authenticated_session


def render_login_view() -> None:
    st.header("Login")
    st.caption("Authenticate to access OpsCenter modules.")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if not submitted:
        return

    if not email or not password:
        st.error("Email and password are required.")
        return

    api_client = st.session_state.get("api_client")
    if api_client is None:
        st.error("API client is unavailable. Check API_BASE_URL and try again.")
        return

    try:
        login_response = api_client.post_form(
            "/auth/login",
            {
                "username": email,
                "password": password,
            },
        )

        access_token = login_response.get("access_token")
        if not access_token:
            st.error("Authentication failed: missing token in response.")
            return

        st.session_state.token = access_token
        me_response = api_client.get("/auth/me")

        role = me_response.get("role") or login_response.get("role")
        if not role:
            st.error("Authentication failed: missing role in response.")
            return

        user = {
            "id": me_response.get("id") or login_response.get("user_id"),
            "name": me_response.get("name") or login_response.get("name"),
            "email": me_response.get("email") or login_response.get("email") or email,
        }
        set_authenticated_session(token=access_token, user=user, role=role)
        st.success("Authenticated successfully.")
        st.rerun()
    except APIClientError as exc:
        st.error(f"Login failed: {exc}")
