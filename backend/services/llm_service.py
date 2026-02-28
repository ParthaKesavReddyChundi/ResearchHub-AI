"""
Async LLM Service with retry logic for ResearchHub AI.

WHY THIS REPLACES groq_client.py:
1. ASYNC: groq_client.py blocks the event loop. This uses asyncio.to_thread()
   so FastAPI can handle other requests while waiting for Groq.
2. RETRY: If Groq rate-limits or has a blip, we retry 3x with exponential backoff
   (1s → 2s → 4s) instead of crashing immediately.
3. FLEXIBLE: Each agent can request different max_tokens — the literature agent
   needs 4000 tokens but the novelty agent only needs 1500.
"""

import asyncio
import logging
from groq import Groq
from config import settings

logger = logging.getLogger(__name__)

# Initialize Groq client once (reused across all calls)
_client = Groq(api_key=settings.GROQ_API_KEY)


def _sync_call(messages: list, max_tokens: int = None) -> str:
    """Synchronous Groq API call (runs inside thread pool)."""
    response = _client.chat.completions.create(
        messages=messages,
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        max_tokens=max_tokens or settings.LLM_MAX_TOKENS,
    )
    return response.choices[0].message.content


async def call_llm_async(
    messages: list,
    max_tokens: int = None,
    retries: int = 3,
    backoff_base: float = 1.0
) -> str:
    """
    Async LLM call with exponential backoff retry.

    Args:
        messages: Chat messages list (system + user)
        max_tokens: Override default max tokens for this call
        retries: Number of retry attempts (default 3)
        backoff_base: Base delay in seconds (doubles each retry)

    Returns:
        LLM response text

    Raises:
        RuntimeError: If all retries are exhausted
    """
    if not messages:
        raise ValueError("messages cannot be empty")

    last_error = None

    for attempt in range(retries):
        try:
            # Run sync Groq call in thread pool (non-blocking)
            result = await asyncio.to_thread(_sync_call, messages, max_tokens)
            return result

        except Exception as e:
            last_error = e
            wait_time = backoff_base * (2 ** attempt)
            logger.warning(
                f"LLM call failed (attempt {attempt + 1}/{retries}): {e}. "
                f"Retrying in {wait_time}s..."
            )

            if attempt < retries - 1:
                await asyncio.sleep(wait_time)

    raise RuntimeError(
        f"LLM call failed after {retries} attempts. Last error: {last_error}"
    )
