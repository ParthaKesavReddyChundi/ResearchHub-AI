"""Full pipeline test — login, create workspace, run analysis."""
import urllib.request
import urllib.parse
import json

BASE = "http://localhost:8000"

# Step 1: Login
login_data = urllib.parse.urlencode({"username": "test@researchhub.ai", "password": "test123"}).encode()
login_req = urllib.request.Request(f"{BASE}/auth/login", data=login_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
login_resp = urllib.request.urlopen(login_req)
token = json.loads(login_resp.read())["access_token"]
print("1. Login OK - got JWT token")

# Step 2: Create workspace
ws_data = json.dumps({"name": "NLP Research"}).encode()
ws_req = urllib.request.Request(f"{BASE}/workspaces/", data=ws_data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
ws_resp = urllib.request.urlopen(ws_req)
workspace = json.loads(ws_resp.read())
ws_id = workspace["id"]
ws_name = workspace["name"]
print(f"2. Workspace created: id={ws_id}, name={ws_name}")

# Step 3: Run full pipeline
print("3. Running full 11-agent pipeline (this takes 30-90 seconds)...")
analyze_data = json.dumps({"query": "transformer attention mechanisms in NLP", "workspace_id": ws_id}).encode()
analyze_req = urllib.request.Request(f"{BASE}/chat/analyze", data=analyze_data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
analyze_resp = urllib.request.urlopen(analyze_req, timeout=300)
result = json.loads(analyze_resp.read())

# Print summary
print(f"\n=== PIPELINE RESULTS ===")
print(f"Query: {result['query']}")
print(f"Pipeline time: {result['pipeline_time_seconds']}s")
r = result["result"]
print(f"Papers found: {r['direct_answer'].get('papers_found', 'N/A')}")
kg = r.get("knowledge_graph", {})
print(f"Knowledge Graph: {kg.get('node_count', 0)} nodes, {kg.get('edge_count', 0)} edges")
print(f"Novelty Score: {r.get('novelty_score', {}).get('overall_score', 'N/A')}/100")
print(f"Confidence: {r.get('confidence_score', {}).get('score', 'N/A')}/100")
print(f"Agents activated: {r.get('explainability_log', {}).get('total_agents', 0)}")

print(f"\n16 Sections check:")
sections = [
    "direct_answer", "context_summary", "knowledge_graph", "comparison",
    "gap_analysis", "deep_insights", "novelty_score", "trend_forecast",
    "recommended_methods_datasets", "experiment_suggestions", "researcher_roadmap",
    "argument_strength", "scientific_critique", "literature_review",
    "confidence_score", "explainability_log"
]
for i, s in enumerate(sections, 1):
    status = "OK" if s in r and r[s] else "EMPTY"
    print(f"  {i:2d}. {s}: {status}")

print("\nDONE - Full pipeline test complete!")
