import streamlit as st


def render_task_form(disabled: bool = False) -> None:
    with st.form("task_form"):
        st.text_input("Task title", disabled=disabled)
        st.text_area("Task description", disabled=disabled)
        st.selectbox("Task status", ["OPEN", "IN_PROGRESS", "DONE"], disabled=disabled)
        st.form_submit_button("Save Task", disabled=disabled)
