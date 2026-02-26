from pydantic import BaseModel
from typing import Optional
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