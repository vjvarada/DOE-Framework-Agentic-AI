"""agent-indian-legal-compliance-agent — MAF Agent definitions.

Automation agent built with DOE Framework.
"""
from __future__ import annotations

import asyncio, os, subprocess, sys
from pathlib import Path
from typing import Any

AGENT_DIR   = Path(__file__).parent.resolve()
PROMPTS_DIR = AGENT_DIR / ".github" / "prompts"
SKILLS_DIR  = AGENT_DIR / ".github" / "skills"
SCRIPTS_DIR = AGENT_DIR / ".tmp" / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def _run_env():
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    scripts = str(SCRIPTS_DIR)
    if existing:
        env["PYTHONPATH"] = scripts + os.pathsep + existing
    else:
        env["PYTHONPATH"] = scripts
    return env


async def _run(args):
    result = await asyncio.to_thread(
        subprocess.run, args, capture_output=True, text=True,
        cwd=str(AGENT_DIR), env=_run_env(),
    )
    if result.returncode != 0:
        raise RuntimeError(
            result.stderr or f"Script exited {result.returncode}")
    return result.stdout or "(no output)"


def _build_system_prompt():
    parts = []
    system_md = PROMPTS_DIR / "system.md"
    if system_md.exists():
        parts.append(
            system_md.read_text(encoding="utf-8", errors="replace"))
    else:
        agents_md = AGENT_DIR / "AGENTS.md"
        if agents_md.exists():
            parts.append(
                agents_md.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


SYSTEM_PROMPT = _build_system_prompt()


async def noop():
    """Placeholder tool — replace with actual skill tools."""
    return "Agent ready. Add skill tools to agents.py."


def _llm_provider():
    base_url = os.environ.get("LITELLM_BASE_URL", "http://127.0.0.1:8080")
    api_key  = os.environ.get("LITELLM_MASTER_KEY", "sk-local")
    return {
        "type": "openai",
        "base_url": base_url + "/v1",
        "api_key": api_key,
    }


def build_agent():
    from agent_framework_github_copilot import GitHubCopilotAgent
    from copilot.types import PermissionHandler

    return GitHubCopilotAgent(
        name="indian-legal-compliance-agent",
        description="Automation agent",
        instructions=SYSTEM_PROMPT,
        tools=[noop],
        default_options={
            "model": "tier-balanced",
            "provider": _llm_provider(),
            "mcp_servers": {},
            "on_permission_request": PermissionHandler.approve_all,
        },
    )


def build_agents():
    return [build_agent()]


__all__ = ["build_agents", "build_agent", "SYSTEM_PROMPT"]
