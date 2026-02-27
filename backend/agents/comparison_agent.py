"""
Comparison Agent — performs cross-paper comparative analysis.

WHY THIS MATTERS:
Individual paper summaries tell you what each paper does.
But researchers need to understand HOW papers relate to each other:
- Which methods overlap vs. diverge?
- What are the performance tradeoffs?
- What are common strengths/weaknesses across the field?

This agent takes the summaries from SummarizerAgent and produces
a side-by-side comparison matrix.
"""

import json
import logging
from typing import List, Dict, Any, Union
from services.llm_service import call_llm_async

logger = logging.getLogger(__name__)


class ComparisonAgent:
    """Agent for performing comparative analysis across research paper summaries."""

    async def run(self, summaries: Union[List[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare multiple research paper summaries.

        Args:
            summaries: Structured summaries from SummarizerAgent

        Returns:
            Dict with comparative analysis or error dict
        """
        if not summaries:
            raise ValueError("summaries cannot be empty")

        # Ensure summaries are serialized as a clean JSON string for the prompt
        summaries_text = json.dumps(summaries, indent=2) if not isinstance(summaries, str) else summaries

        messages = [
            {
                "role": "system",
                "content": "You are an academic research comparison engine."
            },
            {
                "role": "user",
                "content": f"""
                Using these structured summaries:

                {summaries_text}

                Perform comparative analysis across papers.

                Return strictly valid JSON:

                {{
                    "methodology_similarities": [],
                    "methodology_differences": [],
                    "strengths": [],
                    "weaknesses": [],
                    "performance_tradeoffs": []
                }}
                """
            }
        ]

        response = await call_llm_async(messages, max_tokens=1500)

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {str(e)}")
            return {"error": "Invalid JSON", "raw_output": response}