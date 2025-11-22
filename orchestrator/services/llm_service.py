"""
LLM Service - Handles calls to AI providers (Anthropic, OpenAI)
"""

from typing import Optional

from anthropic import Anthropic
from openai import OpenAI

from orchestrator.core.config import settings


class LLMService:
    """
    Service for calling Large Language Models.

    Supports Anthropic (Claude) and OpenAI (GPT) models.
    """

    def __init__(self):
        self.anthropic_client: Optional[Anthropic] = None
        self.openai_client: Optional[OpenAI] = None

        # Initialize clients based on available API keys
        if settings.has_anthropic:
            self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)

        if settings.has_openai:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)

        if not self.anthropic_client and not self.openai_client:
            raise ValueError(
                "No AI provider configured. "
                "Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env"
            )

    async def call(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "claude-sonnet-4.5",
        temperature: float = 0.1,
        max_tokens: int = 16000,
    ) -> str:
        """
        Call LLM with the given prompts.

        Args:
            system_prompt: System prompt (agent expertise)
            user_prompt: User prompt (specific task)
            model: Model to use
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            LLM response text

        Raises:
            ValueError: If model not supported or no API key
        """
        # Determine provider from model name
        if "claude" in model.lower() or "sonnet" in model.lower() or "haiku" in model.lower():
            return await self._call_anthropic(
                system_prompt, user_prompt, model, temperature, max_tokens
            )
        elif "gpt" in model.lower():
            return await self._call_openai(
                system_prompt, user_prompt, model, temperature, max_tokens
            )
        else:
            raise ValueError(f"Unknown model: {model}")

    async def _call_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Call Anthropic API"""
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")

        # Map friendly names to API model IDs
        model_map = {
            "claude-sonnet-4.5": "claude-sonnet-4-20250514",
            "claude-sonnet-4": "claude-sonnet-4-20250514",
            "claude-haiku": "claude-3-5-haiku-20241022",
            "claude-opus": "claude-opus-4-20250514",
        }

        api_model = model_map.get(model, model)

        response = self.anthropic_client.messages.create(
            model=api_model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        return response.content[0].text

    async def _call_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Call OpenAI API"""
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")

        # Map friendly names to API model IDs
        model_map = {
            "gpt-4o": "gpt-4o",
            "gpt-4o-mini": "gpt-4o-mini",
            "gpt-4-turbo": "gpt-4-turbo",
        }

        api_model = model_map.get(model, model)

        response = self.openai_client.chat.completions.create(
            model=api_model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response.choices[0].message.content


# Global LLM service instance
llm_service = LLMService()
