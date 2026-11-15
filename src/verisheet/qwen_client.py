"""Shared OpenAI-compatible Qwen3-8B client used by Planner and semantic Critic."""

from __future__ import annotations
import time
from openai import OpenAI
from verisheet.config import get_settings
from verisheet.schemas import LLMResponse


class QwenClient:
    """Thin, shared API wrapper; roles must supply separate system prompts.

    Public contract:
      `complete(system_prompt: str, user_prompt: str, temperature: float = 0.0,
                max_tokens: int | None = None) -> LLMResponse`

    The wrapper owns endpoint configuration, timeout, normalised token/latency metadata,
    and exception translation. It must not log the API key or unrestricted workbook content.
    """

    def __init__(self, timeout_seconds: int = 45) -> None:
        """Create an OpenAI-compatible client using QWEN_API_BASE and QWEN_API_KEY."""
        settings = get_settings()
        if not settings.qwen_api_base or not settings.qwen_api_key:
            raise ValueError("QWEN_API_BASE and QWEN_API_KEY must be configured")
        self.model = settings.qwen_model
        self.client = OpenAI(
            base_url=settings.qwen_api_base,
            api_key=settings.qwen_api_key,
            timeout=timeout_seconds,
        )

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Call Qwen chat completions and return a normalised response with usage data.

        Args:
            system_prompt: Versioned role instructions (Planner or Critic).
            user_prompt: Bounded, sanitised task context serialized as text/JSON.
            temperature: Use 0 for reproducible planning/critique unless experiment requires otherwise.
            max_tokens: Optional completion cap.
        Returns:
            LLMResponse: content, model, token counts and measured latency.
        Raises:
            RuntimeError: when endpoint communication or response parsing fails.
        """
        started = time.perf_counter()
        try:
            kwargs = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": temperature,
            }
            if max_tokens is not None:
                kwargs["max_tokens"] = max_tokens
            response = self.client.chat.completions.create(**kwargs)
            elapsed_ms = (time.perf_counter() - started) * 1000
            usage = response.usage
            return LLMResponse(
                content=response.choices[0].message.content or "",
                model=getattr(response, "model", self.model),
                input_tokens=getattr(usage, "prompt_tokens", 0) if usage else 0,
                output_tokens=getattr(usage, "completion_tokens", 0) if usage else 0,
                latency_ms=elapsed_ms,
                finish_reason=response.choices[0].finish_reason,
            )
        except Exception as exc:  # Translate provider-specific exceptions at this boundary.
            raise RuntimeError(f"Qwen completion failed: {type(exc).__name__}") from exc
