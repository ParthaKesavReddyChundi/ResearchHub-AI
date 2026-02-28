"""
Intent Router — classifies user queries and decides which agents to activate.

WHY THIS EXISTS:
Not every query needs all 11 agents. For example:
- "Compare transformer vs LSTM" → definitely needs comparison, maybe skip roadmap
- "Give me a research plan for GANs" → needs roadmap, maybe skip critique
- "What's the latest in NLP?" → needs trends, literature, maybe skip gap analysis

HOW IT WORKS NOW:
For v4.0, the full pipeline always runs (all agents activated). The intent
router classifies the query type for logging/explainability but doesn't
yet selectively skip agents. This is the foundation for future selective routing.

FUTURE:
Will use the classification to skip irrelevant agents, saving LLM tokens and time.
"""

import json
import logging
from typing import Dict, Any, List
from services.llm_service import call_llm_async
from agents.system_prompt import INTENT_ROUTER_ROLE

logger = logging.getLogger(__name__)

# All available agents in the pipeline
ALL_AGENTS = [
    "summarizer",
    "comparison",
    "insight",
    "gap",
    "literature",
    "novelty",
    "trend",
    "critique",
    "roadmap",
    "knowledge_graph"
]


class IntentRouter:
    """Routes user queries to appropriate agent(s)."""

    async def classify(self, query: str) -> Dict[str, Any]:
        """
        Classify a user query and determine which agents to activate.

        Args:
            query: The user's research question

        Returns:
            Dict with query_type, intent, and list of agents to activate
        """
        messages = [
            {
                "role": "system",
                "content": INTENT_ROUTER_ROLE
            },
            {
                "role": "user",
                "content": f"""Classify this research query:

"{query}"

Return JSON:
{{
    "query_type": "exploration|comparison|gap_analysis|trend_analysis|critique|roadmap|general",
    "intent": "<one-line description of what the user wants>",
    "primary_focus": "<main topic>"
}}

JSON only."""
            }
        ]

        try:
            response = await call_llm_async(messages, max_tokens=500)
            classification = json.loads(response)
        except Exception as e:
            logger.warning(f"Intent classification failed: {e}, defaulting to general")
            classification = {
                "query_type": "general",
                "intent": query,
                "primary_focus": query
            }

        # For v4.0: always activate all agents (full pipeline)
        # Future versions will selectively route based on query_type
        classification["activated_agents"] = ALL_AGENTS
        classification["routing_strategy"] = "full_pipeline"

        return classification
