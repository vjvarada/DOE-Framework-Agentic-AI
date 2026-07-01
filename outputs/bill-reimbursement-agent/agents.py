"""agent-bill-reimbursement-agent — MAF Agent definitions.

Bill Reimbursement Agent — Processes PDF bills/receipts, extracts data,
summarizes totals by vendor/month, and generates reimbursement PDF reports
and email drafts for submission to accounts teams.

Exports:
    build_agents() -> list[GitHubCopilotAgent]

Architecture (DOE v2):
  Layer 1 (Skills) — .github/skills/*/SKILL.md + scripts/
  Layer 2 (Orchestration) — THIS FILE
  Layer 3 (Execution) — .tmp/scripts/ shared utilities + skill scripts
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
        if SKILLS_DIR.exists():
            skill_sections = []
            for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
                text = skill_md.read_text(
                    encoding="utf-8", errors="replace")
                skill_sections.append(
                    "\n### Tool: " + skill_md.parent.name
                    + "\n\n" + text)
            if skill_sections:
                parts.append(
                    "\n\n---\n\n"
                    "## Registered Skill Tool Descriptions\n")
                parts.extend(skill_sections)
    else:
        agents_md = AGENT_DIR / "AGENTS.md"
        if agents_md.exists():
            parts.append(
                agents_md.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


SYSTEM_PROMPT = _build_system_prompt()


# ── Tool functions ──────────────────────────────────────────────────────


async def extract_bills(input_dir: str, output_path: str) -> str:
    """Extract structured data from PDF bills/receipts in a folder.
    Use when user provides PDF bills for processing.
    input_dir: Path to folder containing PDF bills.
    output_path: Path for output JSON file (e.g. outputs/campaign/step_1_bills.json)."""
    return await _run([sys.executable,
        str(SKILLS_DIR / "bill-extraction" / "scripts" / "extract_bills.py"),
        "--input", input_dir, "--output", output_path])


async def summarize_bills(input_json: str, output_base: str,
                          group_by: str = "vendor") -> str:
    """Summarize extracted bill data into grouped totals and markdown.
    Use after bill extraction to prepare reimbursement summary.
    input_json: Path to the JSON from extract_bills.
    output_base: Base path for output files (e.g. outputs/campaign/step_2).
    group_by: Group bills by 'vendor' or 'month'."""
    return await _run([sys.executable,
        str(SKILLS_DIR / "bill-summarization" / "scripts" / "summarize_bills.py"),
        "--input", input_json, "--output", output_base,
        "--group-by", group_by])


async def generate_bill_summary(input_json: str, output_dir: str,
                                 email_only: str = "false") -> str:
    """Generate PDF reimbursement report and email draft.
    Use when user wants to export a reimbursement report for accounts team.
    input_json: Path to summary JSON from summarize_bills.
    output_dir: Directory for output files.
    email_only: Set to 'true' to skip PDF generation."""
    args = [sys.executable,
        str(SKILLS_DIR / "summary-export" / "scripts" / "generate_bill_summary.py"),
        "--input", input_json, "--output", output_dir]
    if email_only == "true":
        args.append("--email-only")
    return await _run(args)



# ── LiteLLM provider (CommandCenter mode) ────────────────────────────────

def _llm_provider():
    base_url = os.environ.get("LITELLM_BASE_URL", "http://127.0.0.1:8080")
    api_key  = os.environ.get("LITELLM_MASTER_KEY", "sk-local")
    return {
        "type": "openai",
        "base_url": base_url + "/v1",
        "api_key": api_key,
    }


# ── Agent factory ────────────────────────────────────────────────────────

def build_agent():
    from agent_framework_github_copilot import GitHubCopilotAgent
    from copilot.types import PermissionHandler

    return GitHubCopilotAgent(
        name="bill-reimbursement-agent",
        description="Processes PDF bills/receipts, extracts data, summarizes totals, and generates reimbursement PDF reports with email drafts for accounts teams.",
        instructions=SYSTEM_PROMPT,
        tools=[
            extract_bills,
            summarize_bills,
            generate_bill_summary,
        ],
        default_options={
            "model": "tier-balanced",
            "provider": _llm_provider(),
            "mcp_servers": {},
            "on_permission_request": PermissionHandler.approve_all,
        },
    )


def build_agents():
    """Dynamic Agent Loader entry point.
    Synchronous, zero-argument, pure."""
    return [build_agent()]


__all__ = ["build_agents", "build_agent", "SYSTEM_PROMPT"]
