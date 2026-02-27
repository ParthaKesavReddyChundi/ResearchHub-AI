# ResearchHub-AI Frontend — Build Prompt

## You Are Building:
A **premium, visually stunning Streamlit frontend** for ResearchHub-AI — a multi-agent scientific reasoning system that analyzes research topics using 11 AI agents and produces a 16-section deep analysis output.

The backend is **already fully built and running** at `http://localhost:8000`. Your job is to connect a beautiful frontend to it.

---

## DESIGN REQUIREMENTS (CRITICAL — READ FIRST)

### Visual Identity
- **Light tone** — clean white/cream backgrounds with soft pastel accents (lavender, mint, soft blue)
- **NOT a default Streamlit look** — use `st.set_page_config(layout="wide")` + custom CSS to eliminate the default boring Streamlit appearance
- **Premium glass-morphism cards** — frosted glass effect for each of the 16 output sections
- **Subtle gradient accents** — soft linear gradients on headers, buttons, and section dividers
- **Typography** — Use Google Fonts (Inter or Outfit) via CSS injection instead of Streamlit defaults
- **Color palette**: Primary `#6C63FF` (soft indigo), Secondary `#00D2FF` (cyan), Accent `#FF6B9D` (coral pink), Background `#F8F9FE` (off-white), Card `rgba(255,255,255,0.7)` with backdrop blur

### Fluid Movements & Dynamics
- **Smooth fade-in animations** on each section as it appears (CSS `@keyframes fadeInUp`)
- **Animated loading state** — while the pipeline runs (30-90 seconds), show an animated progress indicator with agent names appearing one by one: "🔍 Searching papers..." → "📄 Summarizing..." → "⚖️ Comparing..." → "🧠 Extracting insights..." → "🚧 Finding gaps..." → "🌐 Building knowledge graph..." → "🌟 Scoring novelty..." → "📈 Forecasting trends..." → "🧪 Critiquing methodologies..." → "🗺️ Generating roadmap..." → "📚 Writing literature review..." → "✅ Assembling final output..."
- **Hover effects** on cards — subtle lift + shadow on hover
- **Expandable sections** — each of the 16 sections starts collapsed with a preview, click to expand full content
- **Animated score dials** for Novelty Score (0-100) and Confidence Score (0-100) — circular progress indicators with smooth animation

### Responsiveness
- Desktop-first but should look good on tablet widths
- Use Streamlit columns intelligently — 2-column layout for comparison tables, single column for text-heavy sections
- Sidebar for navigation and settings

### User Experience (A layperson should understand the flow)
- The flow should be IMMEDIATELY obvious: **Enter a research topic → Click Analyze → See beautiful results**
- No technical jargon in the UI — use friendly labels like "What researchers are saying" instead of "Context Summary"
- Each section should have a small emoji icon + one-line description explaining what it shows
- Progress feedback during the 30-90 second pipeline run is CRITICAL — users must know something is happening

---

## BACKEND API REFERENCE

Base URL: `http://localhost:8000`

### Authentication Flow

#### 1. Register
```
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}

Response: {"message": "User registered successfully"}
```

#### 2. Login
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123

Response: {
    "access_token": "eyJhbGci...",
    "token_type": "bearer"
}
```

**IMPORTANT:** Login uses `application/x-www-form-urlencoded` (OAuth2 format), NOT JSON. The field is called `username` even though it's an email.

#### 3. All subsequent requests need auth header:
```
Authorization: Bearer <access_token>
```

### Workspace Management

#### Create Workspace
```
POST /workspaces/
Authorization: Bearer <token>
Content-Type: application/json

{"name": "My Research Project"}

Response: {"id": 1, "name": "My Research Project"}
```

#### List Workspaces
```
GET /workspaces/
Authorization: Bearer <token>

Response: [{"id": 1, "name": "My Research Project"}, ...]
```

#### Delete Workspace
```
DELETE /workspaces/{workspace_id}
Authorization: Bearer <token>

Response: {"message": "Workspace deleted successfully"}
```

### Paper Management

#### Upload Paper
```
POST /papers/{workspace_id}
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <pdf_file>

Response: {"id": 1, "filename": "paper.pdf", "workspace_id": 1}
```

#### List Papers in Workspace
```
GET /papers/{workspace_id}
Authorization: Bearer <token>

Response: [{"id": 1, "filename": "paper.pdf", "workspace_id": 1}, ...]
```

### 🔥 Main Analysis Pipeline (THE KEY ENDPOINT)

#### Run Analysis
```
POST /chat/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
    "query": "transformer attention mechanisms in NLP",
    "workspace_id": 1  // optional — links analysis to workspace for history
}

Response: {
    "query": "transformer attention mechanisms in NLP",
    "pipeline_time_seconds": 25.18,
    "result": { ... 16-section output ... }
}
```

**⚠️ This endpoint takes 30-90 seconds to respond.** Set timeout accordingly.

### Analysis History

#### Get History
```
GET /chat/history/{workspace_id}
Authorization: Bearer <token>

Response: [
    {"id": 1, "query": "transformer attention...", "created_at": "2026-02-27T12:00:00"},
    ...
]
```

#### Get Full Result
```
GET /chat/result/{analysis_id}
Authorization: Bearer <token>

Response: {
    "id": 1,
    "query": "transformer attention...",
    "result": { ... full 16-section JSON ... },
    "created_at": "2026-02-27T12:00:00"
}
```

---

## THE 16-SECTION OUTPUT FORMAT

The `result` field from `/chat/analyze` contains these 16 sections. Each section MUST have its own beautiful card in the UI:

### Section 1: 🔍 Direct Answer
```json
{
    "direct_answer": {
        "query": "the user's question",
        "intent": {"query_type": "exploration", "intent": "...", "primary_focus": "..."},
        "papers_found": 10,
        "sources": {"arxiv": 5, "pubmed": 5}
    }
}
```
**UI:** Hero card at top — show the query, number of papers found, source breakdown (arXiv vs PubMed icons)

### Section 2: 📚 Context Summary
```json
{
    "context_summary": {
        "papers": [
            {"title": "...", "authors": [...], "url": "...", "source": "arxiv", "abstract": "..."}
        ],
        "total_papers": 10
    }
}
```
**UI:** Scrollable paper cards with title, authors, source badge (arXiv/PubMed), clickable URL, truncated abstract with "read more"

### Section 3: 🧠 Knowledge Graph Insights
```json
{
    "knowledge_graph": {
        "node_count": 68,
        "edge_count": 105,
        "key_concepts": [{"name": "...", "centrality": 0.85}],
        "node_type_distribution": {"method": 5, "dataset": 3, ...},
        "clusters": [{"size": 15, "members": ["concept1", ...]}],
        "hidden_connections": [{"from": "A", "to": "B", "via": ["C"], "path_length": 2}],
        "graph_insights": "text summary"
    }
}
```
**UI:** Stats bar (nodes, edges), top concepts as colored tags with centrality bars, hidden connections as a "🔗 Hidden Link" table, cluster visualization

### Section 4: 📊 Comparison Table
```json
{
    "comparison": {
        "methodology_similarities": [...],
        "methodology_differences": [...],
        "strengths": [...],
        "weaknesses": [...],
        "performance_tradeoffs": [...]
    }
}
```
**UI:** Tabbed view — each category as a tab. Items as colored chips (green=similarities, red=differences, blue=strengths, orange=weaknesses)

### Section 5: 🚧 Gap Analysis
```json
{
    "gap_analysis": {
        "repeated_limitations": [...],
        "underexplored_combinations": [...],
        "missing_benchmarks": [...],
        "conflicting_findings": [...],
        "novel_research_directions": [...]
    }
}
```
**UI:** 5 sub-sections with icons. Each gap as a card with severity indicator. Novel directions highlighted with ✨

### Section 6: 💡 Deep Insights
```json
{
    "deep_insights": {
        "unique_methods": [...],
        "common_datasets": [...],
        "evaluation_metrics": [...],
        "recurring_limitations": [...],
        "emerging_themes": [...]
    }
}
```
**UI:** 5-column grid — each insight category as a mini-card with bullet lists

### Section 7: 🌟 Novelty Score
```json
{
    "novelty_score": {
        "overall_score": 78,
        "uniqueness_score": 75,
        "scientific_novelty_score": 80,
        "practical_novelty_score": 70,
        "redundancy_risk_score": 85,
        "opportunity_score": 80,
        "explanation": "...",
        "opportunity_areas": ["area1", "area2"]
    }
}
```
**UI:** Large animated circular gauge (0-100) for overall score. 5 sub-scores as horizontal bars with color coding (red<40, yellow 40-70, green>70). Explanation text below.

### Section 8: 📈 Trend Forecast
```json
{
    "trend_forecast": {
        "current_research_direction": "...",
        "method_adoption_trends": [{"method": "...", "trend": "rising|stable|declining", "reason": "..."}],
        "emerging_tools_and_frameworks": [{"name": "...", "impact": "..."}],
        "one_year_predictions": ["..."],
        "three_year_predictions": ["..."],
        "rising_topics": ["..."],
        "declining_topics": ["..."]
    }
}
```
**UI:** Two-column layout — "1-Year Predictions" vs "3-Year Predictions". Method trends as arrow indicators (↑ rising green, → stable yellow, ↓ declining red). Rising/declining topics as tag clouds.

### Section 9: 🛠️ Recommended Methods & Datasets
```json
{
    "recommended_methods_datasets": {
        "recommended_methods": [...],
        "recommended_datasets": [...],
        "evaluation_metrics": [...]
    }
}
```
**UI:** Three columns — methods, datasets, metrics. Each as a styled pill/chip.

### Section 10: 🧪 Experiment Suggestions
```json
{
    "experiment_suggestions": [
        "Experiment: ...",
        "Explore: ..."
    ]
}
```
**UI:** Numbered list with experiment icons. Each suggestion as a card with "Experiment" or "Explore" badge.

### Section 11: 📘 Researcher Roadmap
```json
{
    "researcher_roadmap": {
        "roadmap": {
            "week_1": {"theme": "...", "tasks": [...], "resources": [...]},
            "week_2": {...},
            "week_3": {...},
            "week_4": {...}
        },
        "project_ideas": [{"title": "...", "difficulty": "beginner|intermediate|advanced", "description": "..."}],
        "recommended_datasets": [{"name": "...", "description": "...", "url": "..."}],
        "baseline_models": [{"name": "...", "description": "...", "implementation": "..."}],
        "key_papers_to_read": [...]
    }
}
```
**UI:** Timeline/stepper view for the 4-week roadmap. Project ideas as difficulty-colored cards (green=beginner, yellow=intermediate, red=advanced). Datasets and models as clickable list items.

### Section 12: 🧩 Argument Strength
```json
{
    "argument_strength": [
        {
            "claim": "...",
            "evidence_strength": "strong|moderate|weak",
            "reliability": "high|medium|low",
            "missing_evidence": "...",
            "bias_indicators": "..."
        }
    ]
}
```
**UI:** Table with color-coded evidence strength (green/yellow/red badges). Each claim as a row.

### Section 13: 🧼 Scientific Critique
```json
{
    "scientific_critique": {
        "strong_points": [{"aspect": "...", "detail": "..."}],
        "weak_points": [{"aspect": "...", "detail": "...", "severity": "minor|moderate|major"}],
        "experimental_design_assessment": "...",
        "reproducibility_assessment": "...",
        "statistical_validity": "...",
        "dataset_quality": "..."
    }
}
```
**UI:** Two-column: Strong Points (green cards) vs Weak Points (red/orange cards with severity badge). Assessment metrics as horizontal progress indicators.

### Section 14: 📚 Literature Review
```json
{
    "literature_review": "Full markdown text with sections: Background, Taxonomy, Comparative Discussion, Key Limitations, Research Gaps, Future Work"
}
```
**UI:** Rendered markdown in a clean reading view with proper headings, paragraphs, and indentation. "Copy to clipboard" button.

### Section 15: 🔐 Confidence Score
```json
{
    "confidence_score": {
        "score": 85,
        "max_score": 100,
        "breakdown": ["Strong paper coverage (8+ papers)", "Summaries generated successfully", ...]
    }
}
```
**UI:** Circular gauge matching novelty score style. Breakdown as a checklist with ✅/⚠️ icons.

### Section 16: 📝 Explainability Log
```json
{
    "explainability_log": {
        "agents_activated": ["intent_router", "summarizer", ...],
        "total_agents": 11,
        "timing_breakdown": {"intent_classification": 1.2, "paper_search": 3.5, ...},
        "total_pipeline_time_seconds": 25.18,
        "routing_strategy": "full_pipeline",
        "reasoning_summary": "Searched arXiv and PubMed for '...', found 10 papers..."
    }
}
```
**UI:** Agent pipeline visualization — show each agent as a node in a horizontal flow with time taken. Total time as a badge. Reasoning summary as collapsible text.

---

## PAGE STRUCTURE

### Page 1: Login / Register
- Clean centered card with email + password fields
- Toggle between "Login" and "Register" modes
- Animated logo at top
- After login, redirect to Dashboard
- Store JWT token in `st.session_state`

### Page 2: Dashboard
- Sidebar: workspace list + "New Workspace" button + user info + logout
- Main area: selected workspace's analysis history
- Each past analysis shown as a card with query text + date + "View Results" button
- Prominent "New Analysis" button or search bar at top

### Page 3: Analysis View (THE MAIN PAGE)
- Large search/query input at top with animated placeholder text
- "Analyze" button with loading animation
- While loading (30-90s): animated agent progress indicator
- After loading: the 16 sections displayed as expandable glass-morphism cards
- Navigation sidebar or sticky section menu for jumping between sections
- "Export as PDF" or "Copy JSON" buttons

### Page 4: Paper Management (Optional)
- Upload PDFs to workspace
- List uploaded papers
- (RAG integration placeholder — show a "Coming Soon: RAG-Enhanced Analysis" badge)

---

## TECHNICAL REQUIREMENTS

1. **Framework:** Streamlit (primary) — if Streamlit CSS limitations are too restrictive for the animations, use Gradio as alternative
2. **HTTP Client:** Use `requests` library to call the backend API
3. **Auth:** Store JWT token in `st.session_state` — include in all API calls as `Authorization: Bearer <token>` header
4. **Timeout:** Set `requests.post(..., timeout=300)` for the `/chat/analyze` endpoint
5. **Error Handling:** Show friendly error messages if backend is unreachable, if auth fails, or if pipeline errors
6. **State Management:** Use `st.session_state` for: token, current workspace, analysis results, current page
7. **Custom CSS:** Inject via `st.markdown('<style>...</style>', unsafe_allow_html=True)` for all custom styling
8. **File Structure:**
```
frontend/
├── app.py              # Main Streamlit app
├── pages/
│   ├── login.py        # Auth page
│   ├── dashboard.py    # Workspace + history
│   └── analysis.py     # Main analysis view
├── components/
│   ├── cards.py        # Reusable card components
│   ├── charts.py       # Score gauges, trend charts
│   ├── animations.py   # CSS animations + loading states
│   └── styles.py       # All custom CSS
├── api/
│   └── client.py       # Backend API client wrapper
└── requirements.txt    # streamlit, requests, plotly
```

9. **Charts:** Use Plotly for interactive charts (novelty gauge, trend arrows, knowledge graph stats)
10. **Backend URL:** Configurable — default `http://localhost:8000`

---

## WHAT SUCCESS LOOKS LIKE

1. A layperson opens the app and IMMEDIATELY knows: "I type a research topic, click Analyze, and get results"
2. The loading animation makes the 30-90 second wait feel engaging, not frustrating
3. The 16-section output looks like a premium research report, not a data dump
4. Every piece of data from the backend is displayed — nothing is hidden or unused
5. The whole app feels like a $200/month SaaS product, not a student project
6. Colors, spacing, typography, and animations are consistent and polished throughout
7. There is a placeholder/badge for "RAG-Enhanced Analysis (Coming Soon)" to indicate future RAG integration from an edge device

---

## IMPORTANT NOTES

- The backend is already running at `http://localhost:8000` — do NOT modify any backend code
- Do NOT create a new backend — only build the frontend that connects to the existing one
- The `/chat/analyze` response takes 30-90 seconds — this is normal (11 AI agents each make LLM calls)
- Focus on making the 16-section output display look EXCEPTIONAL — this is what users see 90% of the time
- The frontend should be placed in `c:\Users\Pardhu\OneDrive\Desktop\Reasearch2\frontend\`
