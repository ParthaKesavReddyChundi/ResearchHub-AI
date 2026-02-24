from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import re
import json
import pdfplumber
from typing import List
from typing_extensions import Annotated

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
    return response.choices[0].message.content


# ---------- COMMON PDF TEXT EXTRACTOR ----------
def extract_pdf_text(uploaded_file: UploadFile):
    with pdfplumber.open(uploaded_file.file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def root():
    return {"message": "ResearchHub AI backend is running 🚀"}


# ---------- GENERAL CHAT ----------
@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    result = call_llm(
        "You are a helpful research assistant.",
        request.message,
        max_tokens=500
    )
    return {"response": result}


# ---------- STRUCTURED SUMMARY ----------
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    full_text = extract_pdf_text(file)

    if not full_text.strip():
        return {"error": "No readable text found in PDF."}

    chunk_size = 3000
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    chunks = chunks[:12]

    chunk_summaries = []

    for chunk in chunks:
        summary = call_llm(
            "Summarize this section of a research paper clearly and concisely.",
            chunk,
            max_tokens=350
        )
        chunk_summaries.append(summary)

    combined_summary = "\n\n".join(chunk_summaries)

    final_summary = call_llm(
        "Create a structured final research summary with:\n1) Problem\n2) Method\n3) Key Contributions\n4) Results.",
        combined_summary,
        max_tokens=700
    )

    return {"summary": final_summary}


# ---------- SIMPLIFY ----------
@app.post("/simplify-pdf")
async def simplify_pdf(file: UploadFile = File(...)):
    full_text = extract_pdf_text(file)
    text = full_text[:8000]

    simplified = call_llm(
        "You simplify research papers into short explanations for beginners.",
        f"""
Simplify into:
- Max 150 words
- Very simple language
- No jargon
- Core idea only

{text}
""",
        max_tokens=300,
        temperature=0.4
    )

    return {"simplified_explanation": simplified}


# ---------- RESEARCH GAPS ----------
@app.post("/research-gaps")
async def research_gaps(file: UploadFile = File(...)):
    full_text = extract_pdf_text(file)

    chunk_size = 3000
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    chunks = chunks[:10]

    summaries = []

    for chunk in chunks:
        summary = call_llm(
            "Summarize this research section.",
            chunk,
            max_tokens=300
        )
        summaries.append(summary)

    combined_summary = "\n".join(summaries)

    gaps = call_llm(
        "Identify research gaps, limitations, and future research directions.",
        combined_summary,
        max_tokens=600,
        temperature=0.4
    )

    return {"research_gaps": gaps}


# ---------- KEY CONTRIBUTIONS ----------
@app.post("/key-contributions")
async def key_contributions(file: UploadFile = File(...)):
    full_text = extract_pdf_text(file)
    text = full_text[:8000]

    contributions = call_llm(
        "Extract structured key contributions.",
        f"""
Identify:
1) Core problem
2) Main innovation
3) Technical contributions
4) Why important

{text}
""",
        max_tokens=500
    )

    return {"key_contributions": contributions}


# ---------- KEYWORDS ----------
@app.post("/extract-keywords")
async def extract_keywords(file: UploadFile = File(...)):
    full_text = extract_pdf_text(file)
    text = full_text[:8000]

    keywords = call_llm(
        "Extract top technical keywords.",
        f"Extract 10-15 important keywords:\n\n{text}",
        max_tokens=300
    )

    return {"keywords": keywords}


# ---------- PAPER COMPARISON ----------
@app.post("/compare-papers")
async def compare_papers(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    text1 = extract_pdf_text(file1)
    text2 = extract_pdf_text(file2)

    summary1 = call_llm("Summarize this paper.", text1[:8000], max_tokens=400)
    summary2 = call_llm("Summarize this paper.", text2[:8000], max_tokens=400)

    comparison = call_llm(
        "Compare two research papers analytically.",
        f"""
Paper 1:
{summary1}

Paper 2:
{summary2}

Compare:
1) Problem
2) Method
3) Results
4) Strengths & weaknesses
5) Impact
""",
        max_tokens=800,
        temperature=0.4
    )

    return {"comparison": comparison}


# ---------- MULTI-FILE LITERATURE REVIEW ----------
# ---------- MULTI-FILE LITERATURE REVIEW ----------
@app.post("/literature-review")
async def literature_review(
    file1: UploadFile = File(None),
    file2: UploadFile = File(None),
    file3: UploadFile = File(None),
    file4: UploadFile = File(None),
    file5: UploadFile = File(None),
):
    files = [file1, file2, file3, file4, file5]
    files = [f for f in files if f is not None]

    if len(files) == 0:
        return {"error": "At least one file required."}

    summaries = []

    for file in files:
        text = extract_pdf_text(file)
        if not text.strip():
            continue

        summary = call_llm(
            "Summarize this research paper clearly.",
            text[:8000],
            max_tokens=400
        )
        summaries.append(summary)

    if not summaries:
        return {"error": "No readable content found."}

    combined = "\n\n".join(summaries)

    review = call_llm(
        "Write a formal academic literature review synthesizing multiple papers.",
        combined,
        max_tokens=1200,
        temperature=0.4
    )

    return {"literature_review": review}

# ---------- LIMITATIONS EXTRACTOR ----------
# ---------- LIMITATIONS EXTRACTOR (STRICT JSON PARSED) ----------
@app.post("/extract-limitations")
async def extract_limitations(file: UploadFile = File(...)):
    full_text = extract_pdf_text(file)

    if not full_text.strip():
        return {"error": "No readable text found in PDF."}

    text = full_text[:15000]

    raw_output = call_llm(
        "Extract limitations in strict JSON format.",
        f"""
Return ONLY valid JSON.
No explanation.
No markdown.
No backticks.

Use this exact structure:

{{
  "computational_constraints": [],
  "data_limitations": [],
  "methodological_limitations": [],
  "experimental_limitations": [],
  "other_limitations": []
}}

Classify limitations carefully into categories.
If none mentioned, leave empty array.

Research Paper:
{text}
""",
        max_tokens=900,
        temperature=0.1
    )

    try:
        parsed = json.loads(raw_output)
    except:
        return {"error": "Model did not return valid JSON.", "raw_output": raw_output}

    return parsed

# ---------- METHOD EXTRACTOR (STRICT JSON PARSED) ----------
@app.post("/extract-method")
async def extract_method(file: UploadFile = File(...)):
    full_text = extract_pdf_text(file)

    if not full_text.strip():
        return {"error": "No readable text found in PDF."}

    text = full_text[:15000]

    raw_output = call_llm(
        "Extract methodological details in strict JSON format.",
        f"""
Return ONLY valid JSON.
No markdown.
No explanation.
No backticks.

Use this exact structure:

{{
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
}}

If any field is not mentioned, leave it empty or null.

Research Paper:
{text}
""",
        max_tokens=900,
        temperature=0.1
    )

    try:
        parsed = json.loads(raw_output)
    except:
        return {"error": "Model did not return valid JSON.", "raw_output": raw_output}

    return parsed

# ---------- RESULTS EXTRACTOR (STRICT JSON) ----------
@app.post("/extract-results")
async def extract_results(file: UploadFile = File(...)):
    full_text = extract_pdf_text(file)

    if not full_text.strip():
        return {"error": "No readable text found in PDF."}

    text = full_text[:15000]

    raw_output = call_llm(
        "Extract experimental results in strict JSON format.",
        f"""
Return ONLY valid JSON.
No markdown.
No explanation.

Structure:

{{
  "datasets": [],
  "evaluation_metrics": [],
  "performance_improvement_percent": null,
  "baseline_model": "",
  "parameter_reduction": null,
  "gpu_memory_requirement": "",
  "training_time_change": ""
}}

Research Paper:
{text}
""",
        max_tokens=900,
        temperature=0.1
    )

    try:
        parsed = json.loads(raw_output)
    except:
        return {"error": "Model did not return valid JSON.", "raw_output": raw_output}

    return parsed

# ---------- METADATA EXTRACTOR (STRICT JSON PARSED) ----------
@app.post("/extract-metadata")
async def extract_metadata(file: UploadFile = File(...)):
    full_text = extract_pdf_text(file)

    if not full_text.strip():
        return {"error": "No readable text found in PDF."}

    text = full_text[:8000]

    raw_output = call_llm(
        "Extract metadata in strict JSON format.",
        f"""
Return ONLY valid JSON.
No explanation.
No markdown.
No backticks.

Use this exact structure:

{{
  "title": "",
  "authors": [],
  "publication_year": null,
  "research_domain": "",
  "task_type": "",
  "keywords": []
}}

Guidelines:
- Extract title from first page.
- Extract author names if available.
- Infer research domain (e.g., Computer Vision, NLP, Robotics).
- Infer task type (e.g., Image Classification, Object Detection, Text Summarization).
- Extract 5–10 important keywords if available.

Research Paper:
{text}
""",
        max_tokens=600,
        temperature=0.1
    )

    try:
        parsed = json.loads(raw_output)
    except:
        return {"error": "Model did not return valid JSON.", "raw_output": raw_output}

    return parsed

# ---------- UNIFIED RESEARCH OBJECT EXTRACTOR (STRICT JSON) ----------
async def extract_research_object(file: UploadFile):
    full_text = extract_pdf_text(file)

    if not full_text.strip():
        return {"error": "No readable text found in PDF."}

    text = full_text[:15000]

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
        max_tokens=1400,
        temperature=0.1
    )

    cleaned = re.sub(r"```json|```", "", raw_output).strip()

    try:
        parsed = json.loads(cleaned)
    except:
        return {"error": "Model did not return valid JSON.", "raw_output": raw_output}

    return parsed

# ---------- FULL RESEARCH AGENT (UNIFIED EXTRACTION + DYNAMIC + ANALYTICS + REFLECTION) ----------
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

    # ---------------- PLANNER ----------------
    plan_raw = call_llm(
        "You are an AI research agent planner.",
        f"""
Goal:
"{goal}"

Available tools:
- extract_research_object
- synthesize_review

Create step-by-step execution plan.

Return ONLY valid JSON:
{{
  "plan": [
    {{"step": 1, "action": ""}}
  ]
}}

No markdown.
No explanation.
""",
        temperature=0.2
    )

    cleaned = re.sub(r"```json|```", "", plan_raw).strip()

    try:
        plan = json.loads(cleaned)
    except:
        return {"error": "Planner failed", "raw_output": plan_raw}

    # ---------------- EXECUTION ----------------
    memory = []

    for file in files:
        paper_memory = {}

        for step in plan.get("plan", []):
            action = step.get("action", "").strip()
            action = action.split()[0]

            if action == "extract_research_object":
                paper_memory = await extract_research_object(file)

        memory.append(paper_memory)

    # ---------------- DETERMINISTIC COMPARISON TABLE ----------------
    comparison_table = []

    for paper in memory:
        metadata = paper.get("metadata", {})
        method = paper.get("method", {})
        results = paper.get("results", {})
        training = method.get("training_strategy", {})

        entry = {
            "title": metadata.get("title"),
            "improvement_percent": results.get("performance_improvement_percent"),
            "optimizer": training.get("optimizer"),
            "epochs": training.get("epochs"),
            "batch_size": training.get("batch_size"),
            "num_datasets": len(results.get("datasets", [])) if results.get("datasets") else 0,
            "parameter_reduction": results.get("parameter_reduction"),
            "gpu_memory_requirement": results.get("gpu_memory_requirement")
        }

        comparison_table.append(entry)

    # Rank by improvement percentage
    comparison_table = sorted(
        comparison_table,
        key=lambda x: x.get("improvement_percent")
        if isinstance(x.get("improvement_percent"), (int, float))
        else -1,
        reverse=True
    )

    # ---------------- SYNTHESIS + REFLECTION ----------------
    final_output = None
    reflection_data = None

    if any(step.get("action", "").startswith("synthesize_review") for step in plan.get("plan", [])):

        initial_analysis = call_llm(
            "You are an autonomous research agent synthesizing structured research data.",
            f"""
Research Goal:
{goal}

Structured Paper Data:
{json.dumps(memory, indent=2)}

Deterministic Comparison Table:
{json.dumps(comparison_table, indent=2)}

Using structured data:

1. Compare methodologies.
2. Compare performance improvements.
3. Rank models by improvement percentage.
4. Identify common limitations.
5. Detect emerging trends.
6. Generate research gaps.
7. Produce formal literature review.

Be analytical and structured.
""",
            max_tokens=1500,
            temperature=0.3
        )

        reflection_raw = call_llm(
            "You are a critical AI research reviewer.",
            f"""
Goal:
{goal}

Analysis:
{initial_analysis}

Check whether:
- All requested components are covered.
- Comparison is explicit.
- Research gaps are meaningful.
- Ranking is justified.

Return ONLY valid JSON:
{{
  "sufficient": true/false,
  "missing_points": []
}}
""",
            temperature=0.1
        )

        cleaned_reflection = re.sub(r"```json|```", "", reflection_raw).strip()

        try:
            reflection_data = json.loads(cleaned_reflection)
        except:
            reflection_data = {"sufficient": True, "missing_points": []}

        if not reflection_data.get("sufficient", True):
            final_output = call_llm(
                "You are refining research analysis.",
                f"""
Goal:
{goal}

Previous Analysis:
{initial_analysis}

Reviewer Feedback:
{reflection_data}

Improve the analysis accordingly.
""",
                max_tokens=1500,
                temperature=0.3
            )
        else:
            final_output = initial_analysis

    return {
        "plan": plan,
        "structured_memory": memory,
        "comparison_table": comparison_table,
        "reflection": reflection_data,
        "final_analysis": final_output
    }