import streamlit as st

from state.session import set_authenticated_session


ROLE_OPTIONS = ["ADMIN", "SUPERVISOR", "OPERATOR"]


def render_login_view() -> None:
    st.header("Login")
    st.caption("Authenticate to access OpsCenter modules.")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ROLE_OPTIONS)
        submitted = st.form_submit_button("Login")

    if submitted:
        if not email or not password:
            st.error("Email and password are required.")
            return

        token = f"mock-token-for-{email}"
        user = {"email": email, "name": email.split("@")[0]}
        set_authenticated_session(token=token, user=user, role=role)
        st.success("Authenticated successfully.")
        st.rerun()
