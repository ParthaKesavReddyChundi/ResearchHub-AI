# 🚀 ResearchHub AI  
### Agentic AI-Powered Research Intelligence System

ResearchHub AI is an **Agentic AI backend system** designed to analyze multiple research papers, extract structured knowledge, compare models, detect research gaps, and automatically generate literature reviews.

This is not just a GenAI summarizer — it is a **plan-driven research agent** with structured memory, deterministic analytics, and reflection-based validation.

---

# 🧠 What Makes This Agentic?

Unlike traditional GenAI systems that only generate text:

✔ Dynamic plan-driven execution  
✔ Tool-based structured extraction  
✔ Deterministic comparison engine  
✔ Model ranking by performance  
✔ Cross-paper structured analytics  
✔ Reflection + self-evaluation step  
✔ Literature review synthesis  

The system behaves like a **research assistant agent**, not just a text generator.

---

# ⚙️ Core Features

### 📄 1. Structured Research Extraction
Extracts:
- Metadata
- Methodology
- Experimental Results
- Limitations

Returns strict JSON.

---

### 📊 2. Deterministic Comparison Engine
Automatically builds:
- Performance ranking table
- Improvement percentage sorting
- Dataset count comparison
- Training configuration comparison

---

### 📚 3. Multi-Paper Literature Review
Upload up to 5 papers →  
System:
- Extracts structured objects
- Compares methodologies
- Identifies trends
- Detects research gaps
- Produces formal literature review

---

### 🤖 4. Dynamic Research Agent (`/research-agent`)
The system:
1. Creates execution plan
2. Calls tools dynamically
3. Builds structured memory
4. Runs deterministic analytics
5. Synthesizes literature review
6. Reflects and improves output

---

# 🏗 Tech Stack

- **FastAPI** (Backend API)
- **Groq LLM (LLaMA 3.3 70B)**
- **Python**
- **Structured JSON extraction**
- **Dynamic planning architecture**

---

# 📂 Project Structure


ResearchHub-AI/
│
├── backend/
│ ├── main.py
│ ├── requirements.txt
│ └── .env (not included in repo)
│
├── frontend/ (optional UI)
│
├── README.md
└── .gitignore


---

# 🚀 Setup Instructions

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ResearchHub-AI.git
cd ResearchHub-AI/backend
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate      # Windows
# OR
source venv/bin/activate   # Mac/Linux
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Add Environment Variables

Create a .env file inside backend/:

GROQ_API_KEY=your_api_key_here

⚠️ Never upload .env to GitHub.

5️⃣ Run the Server
uvicorn main:app --reload

Open browser:

http://127.0.0.1:8000/docs

Swagger UI will appear.

📌 Main API Endpoint
🔬 Research Agent
POST /research-agent
Upload:

1–5 research papers (PDF)

Provide:
Goal: Analyze papers and create literature review with comparison and research gaps.
Output:

Execution plan

Structured memory

Deterministic comparison table

Reflection report

Final literature review

🧠 Example Use Cases

Analyze 20 research papers

Compare CNN vs Transformer architectures

Detect common experimental weaknesses

Identify recurring research gaps

Rank models by improvement %

🛡 Security Notes

.env is ignored

API keys are not committed

Virtual environments are excluded

🎯 Future Roadmap

RAG-based interactive research chat

Persistent research memory

Cross-paper trend analytics

Visualization dashboard

Vector database integration

👨‍💻 Contributors

Built as part of an Agentic AI research intelligence system.

⭐ If You Clone This

Please:

Add your own API key

Do not upload .env

Open issues if you improve architecture


---

# 🔥 What You Should Do Now

1. Replace `YOUR_USERNAME` with your actual GitHub username.
2. Commit the README:

```bash
git add README.md
git commit -m "Added professional README"
git push