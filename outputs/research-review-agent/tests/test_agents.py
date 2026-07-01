"""CommandCenter CI gate."""
import pytest

def test_build_agents_importable():
    import agents  # noqa: F401

def test_build_agents_returns_list():
    try:
        from agents import build_agents
        result = build_agents()
        assert isinstance(result, list) and len(result) >= 1
    except ImportError:
        pytest.skip("MAF runtime not available")

def test_system_prompt_has_content():
    from agents import SYSTEM_PROMPT
    assert len(SYSTEM_PROMPT) > 50
