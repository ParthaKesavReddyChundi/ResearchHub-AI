from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import re
import json
import pdfplumber
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ---------- RAG INITIALIZATION ----------

# ---------- RAG INITIALIZATION (WORKSPACE ISOLATED) ----------

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384

# Workspace dictionary
workspaces = {}

# Load environment variables
load_dotenv()

app = FastAPI(title="ResearchHub AI", version="1.0")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))



# ---------- LLM HELPER FUNCTION ----------
def call_llm(system_prompt, user_prompt, max_tokens=500, temperature=0.3):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Print token usage for monitoring
    print("TOKEN USAGE:", response.usage)

    return response.choices[0].message.content


# ---------- COMMON PDF TEXT EXTRACTOR ----------
def extract_pdf_text(uploaded_file: UploadFile):
    with pdfplumber.open(uploaded_file.file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks




# ---------- PAPER INGESTION FOR RAG ----------
@app.post("/ingest-paper")
async def ingest_paper(workspace_id: str, file: UploadFile = File(...)):

    full_text = extract_pdf_text(file)

    if not full_text.strip():
        return {"error": "No readable text found in PDF."}

    clean_text = re.sub(r"\s+", " ", full_text)
    clean_text = clean_text.replace("", " ")
    clean_text = clean_text.strip()

    chunks = chunk_text(clean_text)

    if not chunks:
        return {"error": "No valid chunks created."}

    embeddings = embedding_model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    if workspace_id not in workspaces:
        workspaces[workspace_id] = {
            "index": faiss.IndexFlatL2(dimension),
            "chunks": [],
            "papers": [],
            "num_vectors": 0
        }

    workspace = workspaces[workspace_id]

    workspace["index"].add(embeddings)
    workspace["chunks"].extend(chunks)
    workspace["papers"].append(file.filename)
    workspace["num_vectors"] += len(chunks)

    return {
        "status": "Paper ingested successfully",
        "workspace_id": workspace_id,
        "num_chunks_added": len(chunks),
        "total_vectors_in_workspace": workspace["num_vectors"]
    }
class QueryRequest(BaseModel):
    question: str
    top_k: int = 6
# ---------- QUERYING WITH RAG ----------
@app.post("/query-paper")
async def query_paper(workspace_id: str, request: QueryRequest):

    if workspace_id not in workspaces:
        return {"error": "Workspace does not exist."}

    workspace = workspaces[workspace_id]

    if workspace["index"].ntotal == 0:
        return {"error": "No papers ingested in this workspace."}

    question_embedding = embedding_model.encode([request.question])
    question_embedding = np.array(question_embedding).astype("float32")

    distances, indices = workspace["index"].search(question_embedding, request.top_k)

    retrieved_chunks = []

    for idx in indices[0]:
        if 0 <= idx < len(workspace["chunks"]):
            retrieved_chunks.append(workspace["chunks"][idx])

    if not retrieved_chunks:
        return {"error": "No relevant chunks found."}

    context = "\n\n".join(retrieved_chunks)

    answer = call_llm(
        "You are a research assistant. Answer strictly using the provided context.",
        f"""
Context:
{context}

Question:
{request.question}

Rules:
- Use ONLY the context.
- If not explicitly mentioned, say: "Insufficient information in the provided paper."
""",
        max_tokens=500,
        temperature=0.2
    )

    return {
        "workspace_id": workspace_id,
        "retrieved_chunks": retrieved_chunks,
        "answer": answer
    }

# ---------- UNIFIED RESEARCH OBJECT EXTRACTOR ----------
async def extract_research_object(file: UploadFile):
    full_text = extract_pdf_text(file)

    if not full_text.strip():
        return {"error": "No readable text found in PDF."}

    text = full_text[:12000]  # reduced safe limit

    raw_output = call_llm(
        "Extract complete structured research object in strict JSON format.",
        f"""
Return ONLY valid JSON.
No explanation.
No markdown.
No backticks.

Structure:

{{
  "metadata": {{
    "title": "",
    "authors": [],
    "publication_year": null,
    "research_domain": "",
    "task_type": "",
    "keywords": []
  }},
  "method": {{
    "model_type": "",
    "architecture_components": [],
    "core_technique": "",
    "training_strategy": {{
        "optimizer": "",
        "learning_rate": "",
        "batch_size": "",
        "epochs": null,
        "regularization": []
    }},
    "unique_innovations": []
  }},
  "results": {{
    "datasets": [],
    "evaluation_metrics": [],
    "performance_improvement_percent": null,
    "baseline_model": "",
    "parameter_reduction": null,
    "gpu_memory_requirement": "",
    "training_time_change": ""
  }},
  "limitations": {{
    "computational_constraints": [],
    "data_limitations": [],
    "methodological_limitations": [],
    "experimental_limitations": [],
    "other_limitations": []
  }}
}}

Research Paper:
{text}
""",
        max_tokens=900,  # reduced from 1400
        temperature=0.1
    )

    cleaned = re.sub(r"```json|```", "", raw_output).strip()

    try:
        parsed = json.loads(cleaned)
    except:
        return {"error": "Invalid JSON returned", "raw_output": raw_output}

    return parsed


# ---------- FULL RESEARCH AGENT (TRUE AGENTIC CONTROLLER) ----------
# ---------- FULL RESEARCH AGENT (AGENTIC v3 - COMPOSITIONAL + CACHED) ----------
@app.post("/research-agent")
async def research_agent(
    goal: str,
    file1: UploadFile = File(None),
    file2: UploadFile = File(None),
    file3: UploadFile = File(None),
    file4: UploadFile = File(None),
    file5: UploadFile = File(None),
):
    files = [file1, file2, file3, file4, file5]
    files = [f for f in files if f is not None]

    if not files:
        return {"error": "At least one file required."}

    # ---------------- AVAILABLE TOOLS (EXPOSED TO PLANNER) ----------------
    AVAILABLE_TOOLS = [
        "extract_metadata",
        "extract_method",
        "extract_results",
        "extract_limitations",
        "synthesize_review"
    ]

    # ---------------- PLANNER ----------------
    plan_raw = call_llm(
        "You are an AI research agent planner.",
        f"""
Goal:
"{goal}"

Available tools:
- extract_metadata
- extract_method
- extract_results
- extract_limitations
- synthesize_review

Choose ONLY from available tools.
Return ONLY valid JSON:

{{ "plan": [{{"step": 1, "action": ""}}] }}

No explanation.
No markdown.
""",
        max_tokens=200,
        temperature=0.2
    )

    cleaned = re.sub(r"```json|```", "", plan_raw).strip()

    try:
        plan = json.loads(cleaned)
    except:
        return {"error": "Planner failed", "raw_output": plan_raw}

    # ---------------- VALIDATE PLAN ----------------
    validated_plan = []
    for step in plan.get("plan", []):
        action = step.get("action")
        if action in AVAILABLE_TOOLS:
            validated_plan.append(action)

    if not validated_plan:
        return {"error": "No valid tools selected by planner."}

    # ---------------- CACHE (UNIFIED EXTRACTION ONLY ONCE PER FILE) ----------------
    extraction_cache = {}
    structured_memory = []

    # If any extraction tool requested, perform unified extraction once
    extraction_tools = [
        "extract_metadata",
        "extract_method",
        "extract_results",
        "extract_limitations"
    ]

    if any(tool in validated_plan for tool in extraction_tools):

        for idx, file in enumerate(files):
            full_object = await extract_research_object(file)

            if "error" in full_object:
                continue

            extraction_cache[idx] = full_object

            paper_data = {}

            if "extract_metadata" in validated_plan:
                paper_data["metadata"] = full_object.get("metadata")

            if "extract_method" in validated_plan:
                paper_data["method"] = full_object.get("method")

            if "extract_results" in validated_plan:
                paper_data["results"] = full_object.get("results")

            if "extract_limitations" in validated_plan:
                paper_data["limitations"] = full_object.get("limitations")

            structured_memory.append(paper_data)

    # ---------------- EARLY EXIT IF NO SYNTHESIS ----------------
    if "synthesize_review" not in validated_plan:
        return {
            "plan": {"plan": validated_plan},
            "structured_memory": structured_memory,
            "note": "Goal completed without synthesis."
        }

    # ---------------- BUILD COMPARISON TABLE (ONLY IF RESULTS AVAILABLE) ----------------
    comparison_table = []

    for paper in extraction_cache.values():
        metadata = paper.get("metadata", {})
        method = paper.get("method", {})
        results = paper.get("results", {})
        training = method.get("training_strategy", {})

        improvement = results.get("performance_improvement_percent")

        entry = {
            "title": metadata.get("title"),
            "improvement_percent": improvement,
            "optimizer": training.get("optimizer"),
            "epochs": training.get("epochs"),
            "batch_size": training.get("batch_size"),
            "num_datasets": len(results.get("datasets", [])),
            "parameter_reduction": results.get("parameter_reduction"),
            "gpu_memory_requirement": results.get("gpu_memory_requirement")
        }

        comparison_table.append(entry)

    comparison_table.sort(
        key=lambda x: x["improvement_percent"]
        if isinstance(x["improvement_percent"], (int, float))
        else -1,
        reverse=True
    )

    # ---------------- SYNTHESIS ----------------
    final_output = call_llm(
        "You are an autonomous research agent synthesizing structured research data.",
        f"""
Research Goal:
{goal}

Structured Data:
{json.dumps(structured_memory)}

Comparison Table:
{json.dumps(comparison_table)}

Generate output strictly aligned with goal.
Be analytical and structured.
""",
        max_tokens=800,
        temperature=0.3
    )

    # ---------------- REFLECTION (ONLY FOR COMPLEX GOALS) ----------------
    reflection_data = None

    if any(keyword in goal.lower() for keyword in ["review", "compare", "rank", "analysis"]):

        reflection_raw = call_llm(
            "You are a critical AI reviewer.",
            f"""
Goal: {goal}

Analysis:
{final_output}

Return ONLY JSON:
{{"sufficient": true/false, "missing_points": []}}
""",
            max_tokens=200,
            temperature=0.1
        )

        cleaned_reflection = re.sub(r"```json|```", "", reflection_raw).strip()

        try:
            reflection_data = json.loads(cleaned_reflection)
        except:
            reflection_data = {"sufficient": True, "missing_points": []}

        if not reflection_data.get("sufficient", True):
            final_output = call_llm(
                "Improve analysis based on reviewer feedback.",
                f"""
Goal: {goal}

Previous Analysis:
{final_output}

Reviewer Feedback:
{reflection_data}
""",
                max_tokens=800,
                temperature=0.3
            )

    return {
        "plan": {"plan": validated_plan},
        "structured_memory": structured_memory,
        "comparison_table": comparison_table,
        "reflection": reflection_data,
        "final_analysis": final_output
    }

