from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime


# ---------------- AUTH ----------------

class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# ---------------- WORKSPACE ----------------

class WorkspaceCreate(BaseModel):
    name: str


class WorkspaceResponse(BaseModel):
    id: int
    name: str


# ---------------- PAPER ----------------

class QueryRequest(BaseModel):
    question: str
    top_k: int = 6


class PaperResponse(BaseModel):
    id: int
    filename: str
    workspace_id: int


# ---------------- CONVERSATION ----------------

class ConversationResponse(BaseModel):
    id: int
    user_message: str
    ai_response: str
    timestamp: datetime


# ---------------- CHAT / ANALYZE ----------------

class ChatRequest(BaseModel):
    """
    Request body for POST /chat/analyze.
    - query: The research question to analyze
    - workspace_id: Optional — links the analysis to a workspace for history
    """
    query: str
    workspace_id: Optional[int] = None


class ChatResponse(BaseModel):
    """
    Wraps the full 16-section pipeline output.
    - query: echoes back the user's input
    - result: the 16-section JSON object
    - pipeline_time_seconds: how long the pipeline took
    """
    query: str
    result: Dict[str, Any]
    pipeline_time_seconds: float
