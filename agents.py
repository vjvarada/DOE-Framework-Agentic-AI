"""agent-creator — MAF Agent definitions.

Agent Creator builds production-ready automation agents using the DOE Framework.
It generates complete, standalone agent workspaces that comply with CommandCenter
agent-repo compatibility standards.

Exports:
    build_agents() -> list[GitHubCopilotAgent]   (Dynamic Agent Loader entry point)

Architecture (DOE v2):
  Layer 1 (Skills)        — .github/skills/*/SKILL.md + .github/skills/*/scripts/
  Layer 2 (Orchestration) — THIS FILE (GitHubCopilotAgent via MAF)
  Layer 3 (Execution)     — .tmp/scripts/ shared utilities + skill scripts
"""
from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

# ── Paths ─────────────────────────────────────────────────────────────────────
AGENT_DIR   = Path(__file__).parent.resolve()
PROMPTS_DIR = AGENT_DIR / ".github" / "prompts"
SKILLS_DIR  = AGENT_DIR / ".github" / "skills"
SCRIPTS_DIR = AGENT_DIR / ".tmp" / "scripts"

# Make .tmp/scripts/ importable by skill scripts at runtime
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


# ── Subprocess helpers ────────────────────────────────────────────────────────

def _run_env() -> dict[str, str]:
    """Add .tmp/scripts/ to PYTHONPATH so skill scripts can import shared utilities."""
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    scripts = str(SCRIPTS_DIR)
    env["PYTHONPATH"] = f"{scripts}{os.pathsep}{existing}" if existing else scripts
    return env


async def _run(args: list[str]) -> str:
    """Run a script as a subprocess. Raises RuntimeError on non-zero exit."""
    result = await asyncio.to_thread(
        subprocess.run, args,
        capture_output=True, text=True,
        cwd=str(AGENT_DIR), env=_run_env(),
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or f"Script exited {result.returncode}")
    return result.stdout or "(no output)"


# ── System prompt ─────────────────────────────────────────────────────────────

def _build_system_prompt() -> str:
    """Load .github/prompts/system.md + append each .github/skills/*/SKILL.md as a tool block."""
    parts: list[str] = []
    system_md = PROMPTS_DIR / "system.md"
    if system_md.exists():
        parts.append(system_md.read_text(encoding="utf-8", errors="replace"))
        if SKILLS_DIR.exists():
            skill_sections: list[str] = []
            for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
                content = skill_md.read_text(encoding="utf-8", errors="replace")
                skill_sections.append(f"\n### Tool: {skill_md.parent.name}\n\n{content}")
            if skill_sections:
                parts.append("\n\n---\n\n## Registered Skill Tool Descriptions\n")
                parts.extend(skill_sections)
    else:
        agents_md = AGENT_DIR / "AGENTS.md"
        if agents_md.exists():
            parts.append(agents_md.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


SYSTEM_PROMPT = _build_system_prompt()


# ── Tool functions ────────────────────────────────────────────────────────────

async def create_agent(name: str, agent_type: str) -> str:
    """Create a new agent workspace. Use when the user asks to create, build, or scaffold a new agent.
    name: Display name for the agent (e.g. "My Sales Agent").
    agent_type: One of lead_generation, email_automation, freelance_proposals, video_editing,
    crm_integration, full_stack, business_planning, research, meeting_minutes,
    legal_compliance, technical_project_planning, hr_management, startup_pr, custom."""
    return await _run([sys.executable,
        str(SKILLS_DIR / "agent-creator" / "scripts" / "create_workspace.py"),
        "--name", name, "--type", agent_type])


async def list_agent_types() -> str:
    """List all available agent types that can be created. Use when the user asks what kinds of
    agents are available or wants to see options before creating one."""
    return await _run([sys.executable,
        str(SKILLS_DIR / "agent-creator" / "scripts" / "create_workspace.py"),
        "--list-types"])


async def upgrade_existing_agent(agent_path: str) -> str:
    """Upgrade an existing agent workspace to comply with current CommandCenter standards.
    Use when the user asks to update, upgrade, or fix an existing agent to meet new compatibility rules.
    agent_path: Path to the agent workspace directory."""
    return await _run([sys.executable,
        str(SKILLS_DIR / "agent-creator" / "scripts" / "upgrade_agent.py"),
        "--path", agent_path])


async def validate_agent(agent_path: str) -> str:
    """Validate an agent workspace against CommandCenter compatibility standards.
    Use when the user wants to check if an agent is properly configured.
    agent_path: Path to the agent workspace directory."""
    return await _run([sys.executable,
        str(SKILLS_DIR / "agent-creator" / "scripts" / "validate_agent.py"),
        "--path", agent_path])


# ── LiteLLM provider (CommandCenter mode) ────────────────────────────────────

def _llm_provider() -> dict[str, Any]:
    base_url = os.environ.get("LITELLM_BASE_URL", "http://127.0.0.1:8080")
    api_key  = os.environ.get("LITELLM_MASTER_KEY", "sk-local")
    return {"type": "openai", "base_url": f"{base_url}/v1", "api_key": api_key}


# ── Agent factory ─────────────────────────────────────────────────────────────

def build_agent() -> "GitHubCopilotAgent":
    from agent_framework_github_copilot import GitHubCopilotAgent  # type: ignore[import]
    from copilot.types import PermissionHandler                     # type: ignore[import]

    return GitHubCopilotAgent(
        name="agent-creator",
        description="Expert agent that creates other agents using the DOE Framework. Builds complete, production-ready agent workspaces with directives, scripts, and automated setup.",
        instructions=SYSTEM_PROMPT,
        tools=[
            create_agent,
            list_agent_types,
            upgrade_existing_agent,
            validate_agent,
        ],
        default_options={
            "model": "tier-balanced",
            "provider": _llm_provider(),
            "mcp_servers": {},
            "on_permission_request": PermissionHandler.approve_all,
        },
    )


def build_agents() -> list:
    """Dynamic Agent Loader entry point. Synchronous, zero-argument, pure."""
    return [build_agent()]


__all__ = ["build_agents", "build_agent", "SYSTEM_PROMPT"]
