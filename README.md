# ResearchHub AI 🚀

ResearchHub AI is an Agentic AI-powered research automation backend designed to go beyond simple chatbot interactions. 

It is built as a tool-using autonomous research agent capable of planning, extracting, comparing, retrieving, validating, and synthesizing academic research papers.

This project focuses on building the intelligence layer of a full-stack research platform.


------------------------------------------------------------
🔷 PROJECT VISION
------------------------------------------------------------

ResearchHub AI is not a chatbot wrapper.

It is an Agentic Research Assistant System that:

• Dynamically plans tool execution  
• Extracts structured research data  
• Performs deterministic comparisons  
• Uses Retrieval-Augmented Generation (RAG)  
• Maintains persistent multi-workspace vector databases  
• Performs reflection-based validation  

The goal is to evolve into a semi-autonomous research assistant platform.


------------------------------------------------------------
🔷 CURRENT ARCHITECTURE
------------------------------------------------------------

Backend: FastAPI  
LLM: Groq (LLaMA 3.3 70B Versatile)  
Embeddings: SentenceTransformers (all-MiniLM-L6-v2)  
Vector DB: FAISS  
Storage: Persistent per-workspace filesystem storage  


------------------------------------------------------------
🔷 FEATURES IMPLEMENTED
------------------------------------------------------------

✅ 1. Unified Structured Research Extraction

Extracts research papers into strict JSON format:

- Metadata
- Method
- Results
- Limitations

Strict JSON enforcement with validation.


------------------------------------------------------------

✅ 2. Agentic Planner System

The /research-agent endpoint:

• Generates execution plan  
• Validates plan against allowed tools  
• Executes only approved tools  
• Builds structured memory  
• Generates deterministic comparison tables  
• Optionally synthesizes analysis  
• Runs reflection loop for validation  

This implements true tool-based Agentic AI logic.


------------------------------------------------------------

✅ 3. Deterministic Comparison Layer

Automatically:

• Ranks models by improvement percentage  
• Compares optimizers  
• Compares epochs  
• Counts datasets  
• Surfaces GPU requirements  

Prevents purely generative comparisons.


------------------------------------------------------------

✅ 4. Multi-Workspace RAG System

• PDF ingestion with chunking + overlap  
• SentenceTransformer embeddings  
• FAISS vector search  
• Workspace isolation  
• Multiple papers per workspace  
• Context-grounded answering  
• Strict anti-hallucination prompt  

Example storage structure:

storage/
    workspace_id/
        index.faiss
        chunks.json
        meta.json


------------------------------------------------------------

✅ 5. Persistent FAISS Storage

• FAISS index saved to disk  
• Chunks saved to disk  
• Metadata saved per workspace  
• Auto-load on server restart  
• Cold-start recovery supported  


------------------------------------------------------------
🔷 ENDPOINTS AVAILABLE
------------------------------------------------------------

POST /ingest-paper  
POST /query-paper  
POST /research-agent  

Additional structured extraction tools are internally supported.


------------------------------------------------------------
🔷 AGENTIC AI DESIGN PRINCIPLES
------------------------------------------------------------

ResearchHub AI follows:

• Dynamic plan-driven execution  
• Tool validation before execution  
• Structured memory building  
• Deterministic reasoning layers  
• Reflection-based output validation  
• Retrieval grounding to prevent hallucination  

This project is architected as a Research Agent System, not a simple LLM interface.


------------------------------------------------------------
🔷 CURRENT LIMITATIONS
------------------------------------------------------------

• No user authentication (JWT not implemented)
• No PostgreSQL database yet
• No conversation history persistence
• No frontend UI (backend only)
• No hybrid keyword + vector search
• Planner still fully LLM-driven


------------------------------------------------------------
🔷 ROADMAP
------------------------------------------------------------

Planned Next Steps:

• PostgreSQL integration  
• JWT-based authentication  
• Workspace-user mapping  
• Conversation persistence  
• Hybrid search (vector + metadata)  
• Planner heuristics improvement  
• Frontend (React + TypeScript + Tailwind)  
• External academic database integration (arXiv, PubMed)  


------------------------------------------------------------
🔷 PROJECT STATUS
------------------------------------------------------------

Backend Intelligence Layer: ~65%  
RAG System: ~75%  
Platform Infrastructure: ~30%  
Frontend: 0%  
Security Layer: 0%  


------------------------------------------------------------
🔷 HOW TO RUN
------------------------------------------------------------

1. Clone the repository
2. Create virtual environment
3. Install requirements
4. Add GROQ_API_KEY to .env
5. Run:

uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs


------------------------------------------------------------

ResearchHub AI is under active development.
The long-term goal is to build a fully autonomous academic research assistant platform.