"""
Agent Orchestrator — the master controller of the ResearchHub AI pipeline.

WHY THIS IS THE MOST IMPORTANT FILE:
This is the "brain" that coordinates all 11 agents and 2 services.
Without this, individual agents are isolated — they can't talk to each other
or combine their outputs. The orchestrator:

1. SEARCHES for papers (paper_search service)
2. CHAINS agents in dependency order (e.g., gap analysis needs summaries first)
3. PARALLELIZES where safe (comparison + insight don't depend on each other)
4. TIMES every step for the explainability log
5. ASSEMBLES the final 16-section output that matches the walkthrough format
6. COMPUTES a confidence score based on data availability
7. GRACEFULLY DEGRADES — if one agent fails, it logs the error and continues
   with fallback results instead of crashing the entire pipeline

PIPELINE DEPENDENCY GRAPH:
    papers → summarizer → comparison → gap → literature
                       → insight    → gap
                       → kg_builder
    query + summaries + insights → novelty, trend, roadmap
    summaries + comparison → critique
    all outputs → 16-section assembly
"""

import asyncio
import time
import logging
from typing import Dict, Any, List

from services.paper_search import search_papers, PaperResult
from services.knowledge_graph import KnowledgeGraphBuilder
from agents.summarizer_agent import SummarizerAgent
from agents.comparison_agent import ComparisonAgent
from agents.insight_agent import InsightAgent
from agents.gap_agent import GapDetectionAgent
from agents.literature_agent import LiteratureReviewAgent
from agents.novelty_agent import NoveltyAgent
from agents.trend_agent import TrendAgent
from agents.critique_agent import CritiqueAgent
from agents.roadmap_agent import RoadmapAgent
from agents.intent_router import IntentRouter

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Master controller that chains all agents into a 16-section pipeline."""

    async def run(self, query: str) -> Dict[str, Any]:
        """
        Execute the full research analysis pipeline.

        Args:
            query: The user's research question

        Returns:
            Dict containing all 16 sections of the output format
        """
        pipeline_start = time.time()
        timing_log = {}
        agents_activated = []

        # ========================================
        # STEP 1: Intent Classification
        # ========================================
        step_start = time.time()
        intent_router = IntentRouter()
        intent = await intent_router.classify(query)
        timing_log["intent_classification"] = round(time.time() - step_start, 2)
        agents_activated.append("intent_router")

        # ========================================
        # STEP 2: Paper Search (arXiv + PubMed)
        # ========================================
        step_start = time.time()
        paper_results: List[PaperResult] = await search_papers(query)
        timing_log["paper_search"] = round(time.time() - step_start, 2)

        if not paper_results:
            return self._empty_result(query, "No papers found for this query")

        # Convert to format expected by agents (objects with title/abstract)
        papers_for_agents = paper_results  # PaperResult has .title and .abstract

        # ========================================
        # STEP 3: Summarizer Agent
        # ========================================
        step_start = time.time()
        summarizer = SummarizerAgent()
        try:
            summaries = await summarizer.run(papers_for_agents)
        except Exception as e:
            logger.error(f"Summarizer agent failed: {e}")
            summaries = {"error": f"Summarizer failed: {str(e)}"}
        timing_log["summarizer"] = round(time.time() - step_start, 2)
        agents_activated.append("summarizer")

        # ========================================
        # STEP 4: Comparison + Insight (PARALLEL)
        # These don't depend on each other, only on summaries.
        # Running them in parallel saves ~50% of this step's time.
        #
        # GRACEFUL DEGRADATION: return_exceptions=True means if one
        # fails, the other still completes. We check each result.
        # ========================================
        step_start = time.time()
        comparison_agent = ComparisonAgent()
        insight_agent = InsightAgent()

        results = await asyncio.gather(
            comparison_agent.run(summaries),
            insight_agent.run(summaries),
            return_exceptions=True
        )

        # Handle comparison result
        if isinstance(results[0], Exception):
            logger.error(f"Comparison agent failed: {results[0]}")
            comparison = {"error": f"Comparison failed: {str(results[0])}"}
        else:
            comparison = results[0]

        # Handle insight result
        if isinstance(results[1], Exception):
            logger.error(f"Insight agent failed: {results[1]}")
            insights = {"error": f"Insight extraction failed: {str(results[1])}"}
        else:
            insights = results[1]

        timing_log["comparison_and_insight"] = round(time.time() - step_start, 2)
        agents_activated.extend(["comparison", "insight"])

        # ========================================
        # STEP 5: Gap Analysis
        # Depends on: summaries, comparison, insights
        # ========================================
        step_start = time.time()
        gap_agent = GapDetectionAgent()
        try:
            gaps = await gap_agent.run(summaries, comparison, insights)
        except Exception as e:
            logger.error(f"Gap agent failed: {e}")
            gaps = {"error": f"Gap analysis failed: {str(e)}"}
        timing_log["gap_analysis"] = round(time.time() - step_start, 2)
        agents_activated.append("gap")

        # ========================================
        # STEP 6: Knowledge Graph + Novelty + Trend + Critique + Roadmap (PARALLEL)
        # These are all independent of each other. Run them concurrently.
        #
        # GRACEFUL DEGRADATION: Each result is checked individually.
        # If novelty fails but roadmap succeeds, the user still gets a roadmap.
        # ========================================
        step_start = time.time()

        kg_builder = KnowledgeGraphBuilder()
        novelty_agent = NoveltyAgent()
        trend_agent = TrendAgent()
        critique_agent = CritiqueAgent()
        roadmap_agent = RoadmapAgent()

        parallel_results = await asyncio.gather(
            kg_builder.build(summaries, insights),
            novelty_agent.run(query, summaries, insights),
            trend_agent.run(query, summaries, insights),
            critique_agent.run(summaries, comparison),
            roadmap_agent.run(query, summaries, gaps),
            return_exceptions=True
        )

        # Unpack with fallbacks
        agent_names = ["knowledge_graph", "novelty", "trend", "critique", "roadmap"]
        fallbacks = [
            {"node_count": 0, "edge_count": 0, "error": "KG build failed"},
            {"overall_score": 0, "explanation": "Novelty scoring failed"},
            {"error": "Trend analysis failed"},
            {"scientific_critique": {"strong_points": [], "weak_points": []}, "argument_strength": []},
            {"error": "Roadmap generation failed"},
        ]

        kg_result, novelty, trend, critique, roadmap = [
            fallbacks[i] if isinstance(r, Exception) else r
            for i, r in enumerate(parallel_results)
        ]

        # Log any failures
        for i, r in enumerate(parallel_results):
            if isinstance(r, Exception):
                logger.error(f"{agent_names[i]} agent failed: {r}")

        timing_log["parallel_agents"] = round(time.time() - step_start, 2)
        agents_activated.extend(agent_names)

        # ========================================
        # STEP 7: Literature Review
        # Depends on: summaries, comparison, insights, gaps
        # ========================================
        step_start = time.time()
        literature_agent = LiteratureReviewAgent()
        try:
            literature_review = await literature_agent.run(summaries, comparison, insights, gaps)
        except Exception as e:
            logger.error(f"Literature agent failed: {e}")
            literature_review = f"Literature review generation failed: {str(e)}"
        timing_log["literature_review"] = round(time.time() - step_start, 2)
        agents_activated.append("literature")

        # ========================================
        # STEP 8: Assemble 16-Section Output
        # ========================================
        pipeline_time = round(time.time() - pipeline_start, 2)

        # Compute confidence score based on data quality
        confidence = self._compute_confidence(
            paper_results, summaries, comparison, insights, gaps
        )

        # Build paper context with URLs
        paper_context = [
            {
                "title": p.title,
                "authors": p.authors,
                "url": p.url,
                "source": p.source,
                "abstract": p.abstract[:200] + "..." if len(p.abstract) > 200 else p.abstract
            }
            for p in paper_results
        ]

        # Extract recommended methods/datasets from insights + gaps
        recommended = self._extract_recommendations(insights, gaps)

        # Extract experiment suggestions from gaps
        experiments = self._extract_experiments(gaps)

        # Assemble the final 16-section output
        result = {
            # Section 1: Direct Answer
            "direct_answer": {
                "query": query,
                "intent": intent,
                "papers_found": len(paper_results),
                "sources": {"arxiv": sum(1 for p in paper_results if p.source == "arxiv"),
                            "pubmed": sum(1 for p in paper_results if p.source == "pubmed")}
            },

            # Section 2: Context Summary
            "context_summary": {
                "papers": paper_context,
                "total_papers": len(paper_results)
            },

            # Section 3: Knowledge Graph Insights
            "knowledge_graph": kg_result,

            # Section 4: Comparison Table
            "comparison": comparison,

            # Section 5: Gap Analysis
            "gap_analysis": gaps,

            # Section 6: Deep Insights
            "deep_insights": insights,

            # Section 7: Novelty Score
            "novelty_score": novelty,

            # Section 8: Trend Forecast
            "trend_forecast": trend,

            # Section 9: Recommended Methods / Datasets
            "recommended_methods_datasets": recommended,

            # Section 10: Experiment Suggestions
            "experiment_suggestions": experiments,

            # Section 11: Researcher Roadmap
            "researcher_roadmap": roadmap,

            # Section 12: Argument Strength Analysis
            "argument_strength": critique.get("argument_strength", []),

            # Section 13: Bias & Critique Review
            "scientific_critique": critique.get("scientific_critique", {}),

            # Section 14: Literature Review
            "literature_review": literature_review,

            # Section 15: Confidence Score
            "confidence_score": confidence,

            # Section 16: Explainability Log
            "explainability_log": {
                "agents_activated": agents_activated,
                "total_agents": len(agents_activated),
                "timing_breakdown": timing_log,
                "total_pipeline_time_seconds": pipeline_time,
                "routing_strategy": intent.get("routing_strategy", "full_pipeline"),
                "reasoning_summary": (
                    f"Searched arXiv and PubMed for '{query}', found {len(paper_results)} papers. "
                    f"Summarized all papers, then ran comparison and insight analysis in parallel. "
                    f"Detected research gaps, built knowledge graph with {kg_result.get('node_count', 0)} nodes, "
                    f"scored novelty at {novelty.get('overall_score', 'N/A')}/100, "
                    f"forecasted trends, critiqued methodologies, and generated a 30-day roadmap. "
                    f"Final confidence: {confidence.get('score', 'N/A')}/100. "
                    f"Total pipeline time: {pipeline_time}s."
                )
            }
        }

        return result

    def _compute_confidence(
        self,
        papers: List[PaperResult],
        summaries: Any,
        comparison: Dict,
        insights: Dict,
        gaps: Dict
    ) -> Dict[str, Any]:
        """
        Compute confidence score (0-100) based on data quality.

        Scoring breakdown:
        - Papers found: 0-30 points (more papers = more evidence)
        - Summaries quality: 0-20 points
        - Comparison depth: 0-20 points
        - Insights richness: 0-15 points
        - Gap detection: 0-15 points
        """
        score = 0
        reasons = []

        # Paper count (30 points max)
        paper_count = len(papers)
        if paper_count >= 8:
            score += 30
            reasons.append("Strong paper coverage (8+ papers)")
        elif paper_count >= 5:
            score += 20
            reasons.append("Moderate paper coverage (5-7 papers)")
        elif paper_count >= 2:
            score += 10
            reasons.append("Limited paper coverage (2-4 papers)")
        else:
            score += 5
            reasons.append("Minimal paper coverage (1 paper)")

        # Summaries quality (20 points)
        if isinstance(summaries, list) and len(summaries) > 0:
            score += 20
            reasons.append("Summaries generated successfully")
        elif isinstance(summaries, dict) and "error" not in summaries:
            score += 15
            reasons.append("Summaries generated with minor issues")
        else:
            score += 5
            reasons.append("Summary generation had issues")

        # Comparison depth (20 points)
        if isinstance(comparison, dict) and "error" not in comparison:
            score += 20
            reasons.append("Comparison analysis complete")
        else:
            score += 5
            reasons.append("Comparison had issues")

        # Insights richness (15 points)
        if isinstance(insights, dict) and "error" not in insights:
            score += 15
            reasons.append("Cross-paper insights extracted")
        else:
            score += 5
            reasons.append("Insight extraction had issues")

        # Gap detection (15 points)
        if isinstance(gaps, dict) and "error" not in gaps:
            score += 15
            reasons.append("Gap analysis complete")
        else:
            score += 5
            reasons.append("Gap analysis had issues")

        return {
            "score": min(score, 100),
            "max_score": 100,
            "breakdown": reasons
        }

    def _extract_recommendations(
        self, insights: Dict, gaps: Dict
    ) -> Dict[str, Any]:
        """Extract recommended methods and datasets from insights + gaps."""
        methods = insights.get("unique_methods", []) if isinstance(insights, dict) else []
        datasets = insights.get("common_datasets", []) if isinstance(insights, dict) else []
        metrics = insights.get("evaluation_metrics", []) if isinstance(insights, dict) else []

        return {
            "recommended_methods": methods,
            "recommended_datasets": datasets,
            "evaluation_metrics": metrics
        }

    def _extract_experiments(self, gaps: Dict) -> List[str]:
        """Extract experiment suggestions from gap analysis."""
        experiments = []

        if isinstance(gaps, dict):
            for direction in gaps.get("novel_research_directions", []):
                if isinstance(direction, str):
                    experiments.append(f"Experiment: {direction}")
                elif isinstance(direction, dict):
                    experiments.append(f"Experiment: {direction.get('description', str(direction))}")

            for combo in gaps.get("underexplored_combinations", []):
                if isinstance(combo, str):
                    experiments.append(f"Explore: {combo}")
                elif isinstance(combo, dict):
                    experiments.append(f"Explore: {combo.get('description', str(combo))}")

        return experiments if experiments else ["No specific experiments suggested — gap data was limited"]

    def _empty_result(self, query: str, reason: str) -> Dict[str, Any]:
        """Return a structured empty result when pipeline can't proceed."""
        return {
            "direct_answer": {"query": query, "error": reason},
            "context_summary": {"papers": [], "total_papers": 0},
            "knowledge_graph": {"node_count": 0, "edge_count": 0},
            "comparison": {},
            "gap_analysis": {},
            "deep_insights": {},
            "novelty_score": {"overall_score": 0, "explanation": reason},
            "trend_forecast": {},
            "recommended_methods_datasets": {},
            "experiment_suggestions": [],
            "researcher_roadmap": {},
            "argument_strength": [],
            "scientific_critique": {},
            "literature_review": "",
            "confidence_score": {"score": 0, "breakdown": [reason]},
            "explainability_log": {
                "agents_activated": [],
                "error": reason
            }
        }