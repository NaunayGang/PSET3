import os
from typing import Any

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


class APIClientError(Exception):
    pass


class APIClient:
    def __init__(self) -> None:
        base_url = os.getenv("API_BASE_URL")
        if not base_url:
            raise APIClientError("API_BASE_URL is not configured. Add it to your environment.")
        self.base_url: str = base_url

    def _build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        token = st.session_state.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        try:
            response = requests.request(
                method=method,
                url=url,
                json=payload,
                headers=self._build_headers(),
                timeout=15,
            )
        except requests.RequestException as exc:
            raise APIClientError(f"Could not connect to backend: {exc}") from exc

        if response.status_code >= 400:
            error_message = "Unexpected API error"
            try:
                error_body = response.json()
                error_message = error_body.get("detail", error_message)
            except ValueError:
                error_message = response.text or error_message
            raise APIClientError(error_message)

        if response.content:
            return response.json()
        return {}

    def get(self, path: str) -> dict[str, Any] | list[Any]:
        return self._request("GET", path)

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any] | list[Any]:
        return self._request("POST", path, payload)

    def patch(self, path: str, payload: dict[str, Any]) -> dict[str, Any] | list[Any]:
        return self._request("PATCH", path, payload)
