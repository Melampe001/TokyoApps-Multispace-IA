"""
AI Router Agent - Intelligent routing between AI providers.

This agent selects the optimal AI provider for each task type:
- Code review → Anthropic (Claude)
- Test generation → OpenAI (o3)
- Documentation → Gemini
- Fast tasks → Groq
"""

import json
import subprocess
from typing import Dict, Any, Literal, Optional

AIProvider = Literal["openai", "anthropic", "gemini", "groq", "llama"]


class AIRouterAgent:
    """Intelligent routing between AI providers."""

    # Task to provider mapping based on strengths
    TASK_ROUTING = {
        "code_review": "anthropic",  # Claude excels at code analysis
        "test_generation": "openai",  # GPT-4/o3 excellent at tests
        "documentation": "gemini",  # Gemini strong at documentation
        "creative": "openai",  # GPT-4 for creative tasks
        "reasoning": "anthropic",  # Claude for deep reasoning
        "fast": "groq",  # Groq for speed
        "multimodal": "gemini",  # Gemini for images/diagrams
        "code_generation": "anthropic",  # Claude for code quality
    }

    # Model selection per provider
    MODEL_SELECTION = {
        "anthropic": {
            "code_review": "claude-opus-4.1",
            "code_generation": "claude-opus-4.1",
            "reasoning": "claude-sonnet-4.5",
            "default": "claude-sonnet-4.5",
        },
        "openai": {
            "test_generation": "o3",
            "creative": "gpt-4",
            "default": "gpt-4-turbo",
        },
        "gemini": {
            "documentation": "gemini-3.0-ultra",
            "multimodal": "gemini-3.0-ultra",
            "default": "gemini-pro",
        },
        "groq": {
            "fast": "llama-3-70b",
            "default": "llama-3-70b",
        },
        "llama": {
            "default": "llama-4-405b",
        },
    }

    def __init__(self, go_binary_path: Optional[str] = None):
        """
        Initialize the AI router agent.

        Args:
            go_binary_path: Path to tokyo-ia Go binary (optional)
        """
        self.go_binary_path = go_binary_path or "./bin/tokyo-ia"

    def route_request(self, task_type: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Route a request to the optimal AI provider.

        Args:
            task_type: Type of task (code_review, test_generation, etc.)
            prompt: The prompt to send to the AI
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            Dictionary with provider, model, response, and metadata
        """
        # Determine optimal provider
        provider = self.TASK_ROUTING.get(task_type, "openai")

        # Get specific model for the task
        model = self._get_model_for_task(provider, task_type)

        # Try calling Go router if available
        try:
            result = self._call_go_router(task_type, prompt, **kwargs)
            if result:
                return result
        except Exception as e:
            print(f"Warning: Could not call Go router: {e}")

        # Return routing decision (actual API call would happen in Go)
        return {
            "provider": provider,
            "model": model,
            "task_type": task_type,
            "prompt_length": len(prompt),
            "routing_reason": self._get_routing_reason(task_type, provider),
            "estimated_cost_usd": self._estimate_cost(provider, len(prompt)),
            "fallback_providers": self._get_fallback_chain(provider),
        }

    def _get_model_for_task(self, provider: str, task_type: str) -> str:
        """Get the optimal model for a provider and task."""
        provider_models = self.MODEL_SELECTION.get(provider, {})
        return provider_models.get(task_type, provider_models.get("default", "unknown"))

    def _get_routing_reason(self, task_type: str, provider: str) -> str:
        """Get human-readable reason for routing decision."""
        reasons = {
            "code_review": f"Claude (Anthropic) excels at code analysis and security review",
            "test_generation": f"OpenAI o3 generates comprehensive test suites",
            "documentation": f"Gemini produces clear, well-structured documentation",
            "creative": f"GPT-4 excels at creative and open-ended tasks",
            "reasoning": f"Claude provides deep logical reasoning",
            "fast": f"Groq provides fastest inference for simple tasks",
            "multimodal": f"Gemini handles images and multimodal content best",
            "code_generation": f"Claude generates high-quality, secure code",
        }
        return reasons.get(
            task_type, f"{provider} selected as default for {task_type}"
        )

    def _estimate_cost(self, provider: str, prompt_length: int) -> float:
        """Estimate cost based on provider and prompt length."""
        # Rough cost estimates per 1000 tokens
        cost_per_1k = {
            "openai": 0.01,
            "anthropic": 0.015,
            "gemini": 0.0005,
            "groq": 0.0002,
            "llama": 0.0,  # Self-hosted
        }

        # Rough token estimation (4 chars per token)
        tokens = prompt_length // 4
        cost = (tokens / 1000) * cost_per_1k.get(provider, 0.01)
        return round(cost, 4)

    def _get_fallback_chain(self, primary_provider: str) -> list:
        """Get fallback providers if primary fails."""
        fallback_chains = {
            "anthropic": ["openai", "gemini", "groq"],
            "openai": ["anthropic", "gemini", "groq"],
            "gemini": ["anthropic", "openai", "groq"],
            "groq": ["llama", "openai"],
            "llama": ["groq", "anthropic"],
        }
        return fallback_chains.get(primary_provider, ["openai"])

    def _call_go_router(
        self, task_type: str, prompt: str, **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Call the Go model router for actual API execution.

        Args:
            task_type: Type of task
            prompt: The prompt
            **kwargs: Additional parameters

        Returns:
            Dictionary with response or None if Go binary not available
        """
        try:
            # Prepare request data
            request_data = {
                "task_type": task_type,
                "prompt": prompt,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2048),
            }

            # Call Go binary (would need to implement ai-route command)
            cmd = [
                self.go_binary_path,
                "ai-route",
                "--task",
                task_type,
                "--prompt",
                prompt[:100],  # Truncate for CLI
            ]

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30
            )

            if result.returncode == 0:
                # Parse JSON response
                response = json.loads(result.stdout)
                return response
            else:
                return None

        except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
            return None

    def get_routing_stats(self) -> Dict[str, Any]:
        """
        Get statistics about routing decisions.

        Returns:
            Dictionary with routing statistics
        """
        return {
            "task_types": list(self.TASK_ROUTING.keys()),
            "providers": list(set(self.TASK_ROUTING.values())),
            "routing_rules": self.TASK_ROUTING,
            "models_available": self.MODEL_SELECTION,
        }

    @classmethod
    def setup(cls) -> Dict[str, Any]:
        """
        Setup the AI router agent (initialization checks).

        Returns:
            Dictionary with setup status
        """
        return {
            "status": "configured",
            "task_routing_rules": cls.TASK_ROUTING,
            "providers_configured": len(set(cls.TASK_ROUTING.values())),
            "models_available": sum(
                len(models) for models in cls.MODEL_SELECTION.values()
            ),
        }
