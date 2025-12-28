"""
Tests for AI Router Agent.
"""

import pytest
from lib.agents.ai_router_agent import AIRouterAgent


def test_router_agent_initialization():
    """Test that router agent initializes correctly."""
    router = AIRouterAgent()
    assert router is not None
    assert router.TASK_ROUTING is not None
    assert router.MODEL_SELECTION is not None


def test_route_request_code_review():
    """Test routing for code review tasks."""
    router = AIRouterAgent()

    result = router.route_request("code_review", "Review this function...")

    assert result is not None
    assert result["provider"] == "anthropic"
    assert result["model"] == "claude-opus-4.1"
    assert result["task_type"] == "code_review"
    assert "routing_reason" in result
    assert "estimated_cost_usd" in result
    assert "fallback_providers" in result


def test_route_request_test_generation():
    """Test routing for test generation tasks."""
    router = AIRouterAgent()

    result = router.route_request("test_generation", "Generate tests for...")

    assert result is not None
    assert result["provider"] == "openai"
    assert result["model"] == "o3"
    assert result["task_type"] == "test_generation"


def test_route_request_documentation():
    """Test routing for documentation tasks."""
    router = AIRouterAgent()

    result = router.route_request("documentation", "Document this API...")

    assert result is not None
    assert result["provider"] == "gemini"
    assert result["model"] == "gemini-3.0-ultra"
    assert result["task_type"] == "documentation"


def test_get_routing_stats():
    """Test getting routing statistics."""
    router = AIRouterAgent()

    stats = router.get_routing_stats()

    assert stats is not None
    assert "task_types" in stats
    assert "providers" in stats
    assert "routing_rules" in stats
    assert "models_available" in stats
    assert len(stats["task_types"]) > 0


def test_setup():
    """Test router setup."""
    result = AIRouterAgent.setup()

    assert result is not None
    assert result["status"] == "configured"
    assert "task_routing_rules" in result
    assert result["providers_configured"] > 0
    assert result["models_available"] > 0


def test_estimate_cost():
    """Test cost estimation."""
    router = AIRouterAgent()

    # Test with different providers
    cost_openai = router._estimate_cost("openai", 1000)
    cost_anthropic = router._estimate_cost("anthropic", 1000)
    cost_gemini = router._estimate_cost("gemini", 1000)

    assert cost_openai > 0
    assert cost_anthropic > 0
    assert cost_gemini > 0
    assert cost_gemini < cost_openai  # Gemini should be cheaper


def test_get_fallback_chain():
    """Test fallback chain generation."""
    router = AIRouterAgent()

    fallback = router._get_fallback_chain("anthropic")

    assert fallback is not None
    assert isinstance(fallback, list)
    assert len(fallback) > 0
    assert "anthropic" not in fallback  # Should not include itself


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
