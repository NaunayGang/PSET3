import streamlit as st

DEFAULT_SESSION_VALUES = {
    "token": None,
    "user": None,
    "role": None,
    "is_authenticated": False,
    "current_view": "Login",
}


def initialize_session_state() -> None:
    for key, value in DEFAULT_SESSION_VALUES.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_authenticated_session(token: str, user: dict, role: str) -> None:
    st.session_state.token = token
    st.session_state.user = user
    st.session_state.role = role
    st.session_state.is_authenticated = True
    st.session_state.current_view = "Incidents"


def clear_authenticated_session() -> None:
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.is_authenticated = False
    st.session_state.current_view = "Login"
