# ResearchHub AI

## Overview

ResearchHub AI is an Agentic AI-powered research assistant platform designed to automate research workflows.

This repository currently contains the **Backend Core Infrastructure**, built using:

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication (OAuth2 Password Flow)

The system provides:

- Secure user authentication
- Workspace management
- Paper metadata management
- Ownership-based access control
- Modular API architecture

---

# Backend Architecture


backend/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── create_tables.py
│
├── routers/
│ ├── auth_router.py
│ ├── workspace_router.py
│ ├── paper_router.py
│
└── requirements.txt


---

# Database Schema

Tables:

- users
- workspaces
- papers
- conversations

Relationships:

- One user → Many workspaces
- One workspace → Many papers
- Ownership enforced via JWT

---

# Setup Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/ParthaKesavReddyChundi/ResearchHub-AI.git
cd ResearchHub-AI/backend
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup PostgreSQL

Create a database named:

researchhub

Create a .env file inside backend/ with:

DATABASE_URL=postgresql://postgres:yourpassword@localhost:5433/researchhub
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
5️⃣ Create Tables
python create_tables.py
6️⃣ Run Server
uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs
API Endpoints
Authentication

POST /auth/register

POST /auth/login

Workspaces

POST /workspaces/

GET /workspaces/

DELETE /workspaces/{id}

Papers

POST /papers/{workspace_id}

GET /papers/{workspace_id}

Security

JWT-based authentication

OAuth2 password flow

Workspace ownership enforcement

Protected endpoints

Project Status

Backend Core Infrastructure: COMPLETE

Next phases:

RAG integration

Paper content extraction

AI Agent orchestration

Frontend integration

Maintainer

Backend Core Engineer:
Partha Kesav Reddy Chundi