#!/usr/bin/env python3
"""
Agent Upgrade Tool

Upgrades an existing agent workspace to comply with the latest
CommandCenter agent-repo compatibility standards.

Usage:
    python upgrade_agent.py --path /path/to/agent
"""

import sys
import json
import argparse
from pathlib import Path


def check_workspace(ws: Path) -> dict:
    """Check what's present and what's missing in the workspace."""
    checks = {
        "has_agents_py": (ws / "agents.py").exists(),
        "has_config_json": (ws / "config.json").exists(),
        "has_github_prompts_system": (ws / ".github" / "prompts" / "system.md").exists(),
        "has_github_skills": (ws / ".github" / "skills").exists(),
        "has_tmp_scripts": (ws / ".tmp" / "scripts").exists(),
        "has_agent_data": (ws / "agent-data").exists(),
        "has_inputs": (ws / "inputs").exists(),
        "has_outputs": (ws / "outputs").exists(),
        "has_tests": (ws / "tests").exists(),
        "has_pyproject_toml": (ws / "pyproject.toml").exists(),
        "has_instructions_md": (ws / "instructions.md").exists(),
        "has_copilot_instructions": (ws / ".github" / "copilot-instructions.md").exists(),
        "has_directives": (ws / "directives").exists(),
        "has_execution": (ws / "execution").exists(),
    }
    return checks


def print_report(ws: Path, checks: dict) -> None:
    """Print a compliance report."""
    print(f"\nAgent Workspace: {ws.name}")
    print(f"Path: {ws}")
    print(f"\n{'=' * 50}")
    print("COMPLIANCE REPORT")
    print(f"{'=' * 50}")

    new_structure = [
        ("agents.py", checks["has_agents_py"]),
        ("config.json", checks["has_config_json"]),
        (".github/prompts/system.md", checks["has_github_prompts_system"]),
        (".github/skills/", checks["has_github_skills"]),
        (".tmp/scripts/", checks["has_tmp_scripts"]),
        ("agent-data/", checks["has_agent_data"]),
        ("inputs/", checks["has_inputs"]),
        ("outputs/", checks["has_outputs"]),
        ("tests/", checks["has_tests"]),
        ("pyproject.toml", checks["has_pyproject_toml"]),
        ("instructions.md", checks["has_instructions_md"]),
        (".github/copilot-instructions.md", checks["has_copilot_instructions"]),
    ]

    old_structure = [
        ("directives/", checks["has_directives"]),
        ("execution/", checks["has_execution"]),
    ]

    print("\nCommandCenter-Required (new standard):")
    all_ok = True
    for name, present in new_structure:
        status = "✓" if present else "✗ MISSING"
        if not present:
            all_ok = False
        print(f"  {status}  {name}")

    print("\nLegacy structure (should be migrated):")
    for name, present in old_structure:
        status = "⚠ PRESENT (needs migration)" if present else "✓ Absent (clean)"
        print(f"  {status}  {name}")

    if all_ok:
        print("\n✓ Agent is fully CommandCenter-compatible.")
    else:
        print("\n⚠ Agent needs upgrading. Use --fix to upgrade.")


def upgrade_workspace(ws: Path) -> None:
    """Upgrade a legacy workspace to CommandCenter-compatible structure."""
    print(f"\nUpgrading: {ws.name}")

    changes = []

    # Create missing folders
    for folder in [
        ".github/prompts", ".github/skills", ".tmp/scripts",
        "agent-data", "inputs", "outputs/_memory", "tests",
    ]:
        p = ws / folder
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            changes.append(f"  + Created {folder}/")

    # Migrate directives → .github/skills/
    directives_dir = ws / "directives"
    if directives_dir.exists():
        for md_file in directives_dir.glob("*.md"):
            skill_name = md_file.stem
            skill_dir = ws / ".github" / "skills" / skill_name
            skill_dir.mkdir(parents=True, exist_ok=True)
            # Create SKILL.md from directive
            content = md_file.read_text(encoding="utf-8", errors="replace")
            frontmatter = f"""---
name: {skill_name}
description: >
  Migrated from directives/{md_file.name}
when_to_use: "User asks about {skill_name.replace('_', ' ')}"
authority: read
cost_tier: 1
version: 0.1.0
---
"""
            (skill_dir / "SKILL.md").write_text(
                frontmatter + "\n" + content, encoding="utf-8")
            # Create scripts dir
            (skill_dir / "scripts").mkdir(exist_ok=True)
            changes.append(
                f"  → Migrated directives/{md_file.name} → "
                f".github/skills/{skill_name}/SKILL.md")

    # Migrate execution/ scripts → .tmp/scripts/ (shared)
    execution_dir = ws / "execution"
    if execution_dir.exists():
        tmp_scripts = ws / ".tmp" / "scripts"
        tmp_scripts.mkdir(parents=True, exist_ok=True)
        for py_file in execution_dir.glob("*.py"):
            dest = tmp_scripts / py_file.name
            if not dest.exists():
                content = py_file.read_bytes()
                dest.write_bytes(content)
                changes.append(
                    f"  → Copied execution/{py_file.name} → "
                    f".tmp/scripts/{py_file.name}")

    # Create agents.py if missing
    if not (ws / "agents.py").exists():
        slug = ws.name.replace(" ", "-").lower()
        (ws / "agents.py").write_text(f'''"""agent-{slug} — MAF Agent definitions.

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
            result.stderr or f"Script exited {{result.returncode}}")
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
    return "\\n".join(parts)


SYSTEM_PROMPT = _build_system_prompt()


async def noop():
    """Placeholder tool — replace with actual skill tools."""
    return "Agent ready. Add skill tools to agents.py."


def _llm_provider():
    base_url = os.environ.get("LITELLM_BASE_URL", "http://127.0.0.1:8080")
    api_key  = os.environ.get("LITELLM_MASTER_KEY", "sk-local")
    return {{
        "type": "openai",
        "base_url": base_url + "/v1",
        "api_key": api_key,
    }}


def build_agent():
    from agent_framework_github_copilot import GitHubCopilotAgent
    from copilot.types import PermissionHandler

    return GitHubCopilotAgent(
        name="{slug}",
        description="Automation agent",
        instructions=SYSTEM_PROMPT,
        tools=[noop],
        default_options={{
            "model": "tier-balanced",
            "provider": _llm_provider(),
            "mcp_servers": {{}},
            "on_permission_request": PermissionHandler.approve_all,
        }},
    )


def build_agents():
    return [build_agent()]


__all__ = ["build_agents", "build_agent", "SYSTEM_PROMPT"]
''')
        changes.append("  + Created agents.py")

    # Create config.json if missing
    if not (ws / "config.json").exists():
        slug = ws.name.replace(" ", "-").lower()
        cfg = {
            "name": slug,
            "description": "Automation agent",
            "version": "0.1.0",
            "skill_repos": [],
            "integrations": [],
            "optional_integrations": [],
            "tags": ["automation"],
            "tool_scope": None,
            "max_mutation_attempts": 1,
            "mcp_servers": {},
            "icon": "Bot",
            "category": "external",
            "webhook_routes": [],
        }
        with open(ws / "config.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        changes.append("  + Created config.json")

    # Create .github/prompts/system.md if missing
    prompts_dir = ws / ".github" / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    if not (prompts_dir / "system.md").exists():
        (prompts_dir / "system.md").write_text(
            f"# {ws.name} — System Prompt\n\n"
            "## Purpose\n\nAutomation agent built with DOE Framework.\n\n"
            "## Rules\n\n"
            "1. Read relevant SKILL.md before running scripts.\n"
            "2. Use scripts for deterministic work.\n"
            "3. Raise errors explicitly.\n",
            encoding="utf-8")
        changes.append("  + Created .github/prompts/system.md")

    # Create copilot-instructions.md
    ci = ws / ".github" / "copilot-instructions.md"
    if not ci.exists():
        ci.write_text(
            f"# {ws.name} — Copilot Instructions\n\n"
            "Built with DOE Framework. CommandCenter-compatible.\n",
            encoding="utf-8")
        changes.append("  + Created .github/copilot-instructions.md")

    # Create instructions.md
    instr = ws / "instructions.md"
    if not instr.exists():
        instr.write_text(
            f"# {ws.name} — Brief\n\nAutomation agent.\n", encoding="utf-8")
        changes.append("  + Created instructions.md")

    # Create agent-data/INDEX.md
    idx = ws / "agent-data" / "INDEX.md"
    if not idx.exists():
        idx.parent.mkdir(parents=True, exist_ok=True)
        idx.write_text(
            "# Agent Data — Index\n\n"
            "| Path | Purpose | Usage |\n"
            "|------|---------|-------|\n",
            encoding="utf-8")
        changes.append("  + Created agent-data/INDEX.md")

    # Create tests/test_agents.py
    test_file = ws / "tests" / "test_agents.py"
    if not test_file.exists():
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(
            '"""CommandCenter CI gate."""\n'
            'import pytest\n\n'
            'def test_build_agents_importable():\n'
            '    import agents  # noqa: F401\n\n'
            'def test_build_agents_returns_list():\n'
            '    try:\n'
            '        from agents import build_agents\n'
            '        result = build_agents()\n'
            '        assert isinstance(result, list) and len(result) >= 1\n'
            '    except ImportError:\n'
            '        pytest.skip("MAF runtime not available")\n\n'
            'def test_system_prompt_has_content():\n'
            '    from agents import SYSTEM_PROMPT\n'
            '    assert len(SYSTEM_PROMPT) > 50\n',
            encoding="utf-8")
        changes.append("  + Created tests/test_agents.py")

    # Create pyproject.toml
    ppt = ws / "pyproject.toml"
    if not ppt.exists():
        ppt.write_text(
            '[project]\n'
            'name = "automation-agent"\n'
            'version = "0.1.0"\n'
            'requires-python = ">=3.11"\n'
            'dependencies = ["requests", "python-dotenv"]\n\n'
            '[project.optional-dependencies]\n'
            'dev = ["pytest>=8", "pytest-asyncio>=0.24"]\n\n'
            '[build-system]\n'
            'requires = ["hatchling"]\n'
            'build-backend = "hatchling.build"\n\n'
            '[tool.pytest.ini_options]\n'
            'asyncio_mode = "auto"\n'
            'testpaths = ["tests"]\n',
            encoding="utf-8")
        changes.append("  + Created pyproject.toml")

    # Create inputs/.gitkeep
    inputs_gk = ws / "inputs" / ".gitkeep"
    if not inputs_gk.exists():
        inputs_gk.parent.mkdir(parents=True, exist_ok=True)
        inputs_gk.write_text("")
        changes.append("  + Created inputs/.gitkeep")

    print("\nChanges made:")
    if changes:
        for c in changes:
            print(c)
    else:
        print("  (no changes needed — already compliant)")

    print(f"\n✓ Upgrade complete for: {ws.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Upgrade agent workspace to CommandCenter standards")
    parser.add_argument("--path", required=True,
                        help="Path to agent workspace directory")
    parser.add_argument("--fix", action="store_true",
                        help="Apply fixes to upgrade the workspace")
    args = parser.parse_args()

    ws = Path(args.path).resolve()
    if not ws.exists():
        print(f"Error: Path not found: {ws}")
        sys.exit(1)

    checks = check_workspace(ws)

    if args.fix:
        upgrade_workspace(ws)
    else:
        print_report(ws, checks)
        print("\nRun with --fix to apply upgrades.")


if __name__ == "__main__":
    main()
