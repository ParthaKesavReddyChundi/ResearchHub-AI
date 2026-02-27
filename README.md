# ResearchHub AI

An **Agentic AI-powered research assistant platform** that automates scientific reasoning workflows through multi-agent orchestration.

---

## Project Structure

```
ResearchHub-AI/
│
├── backend/              # FastAPI multi-agent analysis system
│   ├── main.py           # FastAPI entry point (v4.0)
│   ├── config.py         # Centralized env settings (Pydantic)
│   ├── database.py       # SQLAlchemy + PostgreSQL
│   ├── models.py         # DB models (users, workspaces, papers, analysis_results)
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── auth.py           # JWT + bcrypt authentication
│   ├── create_tables.py  # DB init script
│   ├── test_pipeline.py  # End-to-end pipeline test
│   ├── requirements.txt
│   ├── routers/          # API endpoints (auth, workspace, paper, chat)
│   ├── agents/           # 11 AI agents (summarizer, comparison, gap, etc.)
│   │   └── orchestrator.py  # Master controller chaining all agents
│   └── services/         # LLM, paper search (arXiv + PubMed), knowledge graph
│
├── frontend/             # Streamlit UI
│   ├── app.py            # Main Streamlit entry point
│   ├── requirements.txt
│   ├── api/              # Backend API client wrapper
│   ├── components/       # Reusable UI components (cards, charts, animations, styles)
│   └── views/            # Page views (login, dashboard, analysis, papers)
│
├── graph_rag/            # Graph RAG pipeline (PDF → Neo4j Knowledge Graph)
│   ├── pipeline.py       # Full data ingestion pipeline
│   ├── graph_rag.py      # Interactive Q&A system over the knowledge graph
│   ├── test_pipeline.py  # Quick test (3 chunks only)
│   ├── docker-compose.yml # Neo4j Docker setup
│   ├── requirements.txt
│   ├── .env.example
│   └── files/            # PDF files for ingestion
│
├── docs/                 # Documentation
│   └── FRONTEND_PROMPT.md   # Frontend design specification
│
├── .env.example          # Environment variable template (all components)
├── .gitignore
└── README.md
```

---

## Components

### 1. Backend — Multi-Agent Analysis System

A FastAPI server with **11 AI agents** that analyze research topics and produce a **16-section deep analysis output**.

**Tech Stack:** FastAPI, PostgreSQL, SQLAlchemy, JWT Auth, Groq LLM (Llama 3.3)

**Setup:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Create .env with:
# DATABASE_URL=postgresql://postgres:yourpassword@localhost:5433/researchhub
# SECRET_KEY=your_secret_key
# GROQ_API_KEY=your_groq_api_key

python create_tables.py
uvicorn main:app --reload
```

**API Docs:** http://127.0.0.1:8000/docs

### 2. Frontend — Streamlit UI

A premium Streamlit interface connecting to the backend API.

**Setup:**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 3. Graph RAG Pipeline

Standalone pipeline that ingests PDFs, extracts entities/relationships via LLM, and stores them in a Neo4j knowledge graph for Q&A.

**Setup:**
```bash
cd graph_rag

# Start Neo4j via Docker
docker compose up -d

# Create .env (copy from .env.example)
pip install -r requirements.txt

# Run the ingestion pipeline
python pipeline.py

# Interactive Q&A
python graph_rag.py
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/auth/register` | POST | Register new user |
| `/auth/login` | POST | Login (returns JWT) |
| `/workspaces/` | POST/GET/DELETE | Workspace CRUD |
| `/papers/{workspace_id}` | POST/GET | Paper upload & listing |
| `/chat/analyze` | POST | Run 11-agent analysis pipeline |
| `/chat/history/{workspace_id}` | GET | Analysis history |
| `/chat/result/{analysis_id}` | GET | Full analysis result |

---

## Maintainer

**Partha Kesav Reddy Chundi**