"""
ResearchHub-AI — Backend API Client
Wraps all HTTP interactions with the FastAPI backend.
"""

import requests
from typing import Optional, Dict, Any, List


class ResearchHubAPI:
    """Client for the ResearchHub AI backend API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    def _headers(self, token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    # ── Authentication ──────────────────────────────────────────────

    def register(self, email: str, password: str) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base_url}/auth/register",
            json={"email": email, "password": password},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login uses OAuth2 form-encoded format (username field = email)."""
        resp = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    # ── Workspaces ──────────────────────────────────────────────────

    def list_workspaces(self, token: str) -> List[Dict[str, Any]]:
        resp = requests.get(
            f"{self.base_url}/workspaces/",
            headers=self._headers(token),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def create_workspace(self, token: str, name: str) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base_url}/workspaces/",
            headers=self._headers(token),
            json={"name": name},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def delete_workspace(self, token: str, workspace_id: int) -> Dict[str, Any]:
        resp = requests.delete(
            f"{self.base_url}/workspaces/{workspace_id}",
            headers=self._headers(token),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    # ── Papers ──────────────────────────────────────────────────────

    def upload_paper(self, token: str, workspace_id: int, file) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base_url}/papers/{workspace_id}",
            headers=self._headers(token),
            files={"file": file},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()

    def list_papers(self, token: str, workspace_id: int) -> List[Dict[str, Any]]:
        resp = requests.get(
            f"{self.base_url}/papers/{workspace_id}",
            headers=self._headers(token),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    # ── Analysis ────────────────────────────────────────────────────

    def run_analysis(
        self, token: str, query: str, workspace_id: Optional[int] = None
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"query": query}
        if workspace_id is not None:
            payload["workspace_id"] = workspace_id
        resp = requests.post(
            f"{self.base_url}/chat/analyze",
            headers=self._headers(token),
            json=payload,
            timeout=300,
        )
        resp.raise_for_status()
        return resp.json()

    def get_history(self, token: str, workspace_id: int) -> List[Dict[str, Any]]:
        resp = requests.get(
            f"{self.base_url}/chat/history/{workspace_id}",
            headers=self._headers(token),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def get_result(self, token: str, analysis_id: int) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.base_url}/chat/result/{analysis_id}",
            headers=self._headers(token),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
