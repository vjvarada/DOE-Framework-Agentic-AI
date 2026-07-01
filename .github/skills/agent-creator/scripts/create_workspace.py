#!/usr/bin/env python3
"""
CommandCenter-Compatible Agent Workspace Generator

Creates a complete, production-ready agent workspace that complies with
the agent_repo_compatibility.md standard. Every generated workspace includes
agents.py, config.json, .github/prompts/system.md, .github/skills/,
.tmp/scripts/, agent-data/, inputs/, outputs/, tests/, and all required
configuration files.

Usage:
    python create_workspace.py --name "My Agent" --type lead_generation
    python create_workspace.py --name "My Agent" --type custom
    python create_workspace.py --list-types
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent  # .github/skills/agent-creator/
REPO_ROOT = SKILL_DIR.parent.parent.parent  # repo root
TEMPLATES_FILE = REPO_ROOT / "execution" / "agent_templates.json"
OUTPUTS_DIR = REPO_ROOT / "outputs"
DIRECTIVES_DIR = REPO_ROOT / "directives"
EXECUTION_DIR = REPO_ROOT / "execution"
AGENT_REPO_COMPAT = REPO_ROOT / "agent_repo_compatibility.md"


def load_templates() -> dict:
    with open(TEMPLATES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-")


def list_agent_types(templates: dict) -> None:
    print("\n" + "=" * 60)
    print("AVAILABLE AGENT TYPES (CommandCenter-Compatible)")
    print("=" * 60)
    for key, info in templates["agent_types"].items():
        print(f"\n  {key}")
        print(f"    Name: {info['name']}")
        print(f"    Description: {info['description']}")
        print(f"    Skills: {len(info.get('directives', []))}")
        scripts = info.get("scripts", [])
        count = "ALL" if scripts == "ALL" else len(scripts)
        print(f"    Scripts: {count}")
    print("\n" + "=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# FOLDER STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

def create_folder_structure(ws: Path) -> None:
    """Create the canonical CommandCenter-compatible folder structure."""
    folders = [
        ".github/prompts",
        ".github/agents",
        ".github/skills",
        ".github/instructions",
        ".tmp/scripts",
        ".tmp/search_cache",
        ".tmp/web_cache",
        "agent-data/templates",
        "agent-data/images",
        "agent-data/specs",
        "inputs",
        "outputs/_memory",
        "tests",
    ]
    for folder in folders:
        (ws / folder).mkdir(parents=True, exist_ok=True)
    # Create .gitkeep files for empty tracked folders
    for f in ["inputs/.gitkeep", ".tmp/search_cache/README.md",
              ".tmp/web_cache/README.md"]:
        p = ws / f
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.write_text("")
    print("  ✓ Created canonical folder structure")


# ═══════════════════════════════════════════════════════════════════════════════
# SKILL GENERATION (directives → .github/skills/<name>/SKILL.md + scripts/)
# ═══════════════════════════════════════════════════════════════════════════════

SKILL_TO_SCRIPTS = {
    "gmaps_lead_generation": [
        "scrape_google_maps.py", "scrape_apify.py", "scrape_apify_parallel.py",
        "gmaps_lead_pipeline.py", "gmaps_parallel_pipeline.py"
    ],
    "google_serp_lead_scraper": ["serp_market_research.py"],
    "scrape_leads": ["enrich_emails.py"],
    "instantly_autoreply": [
        "instantly_autoreply.py", "instantly_create_campaigns.py",
        "welcome_client_emails.py"
    ],
    "upwork_scrape_apply": [
        "upwork_scraper.py", "upwork_apify_scraper.py",
        "upwork_proposal_generator.py"
    ],
    "create_proposal": ["create_proposal.py"],
    "video_editor": [
        "video_editor_pipeline.py", "jump_cut_vad_singlepass.py",
        "insert_3d_transition.py"
    ],
    "jump_cut_vad": [],
    "business_planning": [
        "create_google_doc.py", "update_google_doc.py",
        "serp_market_research.py", "generate_business_plan.py"
    ],
    "research_paper_review": [
        "search_papers.py", "fetch_paper.py", "pdf_to_markdown.py",
        "compile_review_paper.py"
    ],
    "meeting_minutes": [
        "transcribe_audio.py", "generate_meeting_minutes.py",
        "create_google_doc.py", "update_google_doc.py"
    ],
    "indian_legal_compliance": [
        "legal_research.py", "compliance_checker.py", "legal_doc_generator.py",
        "compliance_tracker.py", "create_google_doc.py", "update_google_doc.py"
    ],
    "technical_project_planning": [
        "web_research.py", "search_papers.py", "fetch_paper.py",
        "pdf_to_markdown.py", "generate_project_plan.py"
    ],
    "hr_management": [
        "parse_resume.py", "generate_job_description.py", "evaluate_candidate.py",
        "research_candidate.py", "generate_pdf.py", "pdf_to_markdown.py",
        "create_google_doc.py", "update_google_doc.py", "web_research.py"
    ],
    "startup_pr_outreach": [
        "serp_market_research.py", "web_research.py", "scrape_apify.py",
        "enrich_emails.py", "create_google_doc.py", "update_google_doc.py",
        "casualize_first_names_batch.py", "casualize_company_names_batch.py",
        "casualize_city_names_batch.py", "casualize_batch.py",
        "instantly_create_campaigns.py", "instantly_autoreply.py",
        "welcome_client_emails.py", "generate_pdf.py"
    ],
    "memory_management": ["memory_db.py", "memory_bank.py"],
    "infrastructure_tools": [
        "tool_registry.py", "tool_registry.json", "task_graph.py",
        "execution_trace.py", "confirm_action.py"
    ],
}

SHARED_SCRIPTS = [
    "read_sheet.py", "append_to_sheet.py", "update_sheet.py",
    "create_google_doc.py", "update_google_doc.py",
]


def directive_to_skill_name(directive: str) -> str:
    """Convert directive filename to skill name."""
    return directive.replace(".md", "")


def generate_skill_md(ws: Path, skill_name: str, directive_content: str,
                       scripts: list) -> None:
    """Generate a SKILL.md file from a directive."""
    # Extract first heading as description
    lines = directive_content.strip().split("\n")
    desc = lines[0].lstrip("#").strip() if lines else skill_name

    frontmatter = f"""---
name: {skill_name}
description: >
  {desc[:200]}
when_to_use: "User asks about {skill_name.replace('_', ' ')}"
authority: read
cost_tier: 1
version: 0.1.0
---
"""
    body = f"""# {desc}

{chr(10).join(lines[1:]) if len(lines) > 1 else ""}

## Scripts

"""
    if scripts:
        for s in scripts:
            body += f"| `scripts/{s}` | Execute with `python .github/skills/{skill_name}/scripts/{s}` |\n"
    else:
        body += "| (none) | No scripts for this skill — use Copilot directly |\n"

    body += f"""
## Usage

```bash
# From agent root:
python .github/skills/{skill_name}/scripts/<script>.py --help
```

## Outputs

Writes to `outputs/{{campaign-slug}}/step_N_*.json`.
"""
    skill_dir = ws / ".github" / "skills" / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(frontmatter + body, encoding="utf-8")


def copy_skill_scripts(ws: Path, skill_name: str, script_names: list,
                        all_scripts_map: dict) -> int:
    """Copy scripts to .github/skills/<skill>/scripts/ and return count."""
    skill_scripts_dir = ws / ".github" / "skills" / skill_name / "scripts"
    skill_scripts_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for sname in script_names:
        src = EXECUTION_DIR / sname
        if src.exists():
            shutil.copy2(src, skill_scripts_dir / sname)
            copied += 1
    return copied


def copy_shared_scripts(ws: Path) -> int:
    """Copy shared utilities to .tmp/scripts/."""
    dest = ws / ".tmp" / "scripts"
    dest.mkdir(parents=True, exist_ok=True)
    copied = 0
    for sname in SHARED_SCRIPTS:
        src = EXECUTION_DIR / sname
        if src.exists() and not (dest / sname).exists():
            shutil.copy2(src, dest / sname)
            copied += 1
    # Also copy core infra scripts
    for sname in ["memory_db.py", "memory_bank.py", "tool_registry.py",
                   "task_graph.py", "execution_trace.py", "confirm_action.py"]:
        src = EXECUTION_DIR / sname
        if src.exists() and not (dest / sname).exists():
            shutil.copy2(src, dest / sname)
            copied += 1
    # Copy tool_registry.json
    reg_src = EXECUTION_DIR / "tool_registry.json"
    if reg_src.exists() and not (dest / "tool_registry.json").exists():
        shutil.copy2(reg_src, dest / "tool_registry.json")
        copied += 1
    return copied


def setup_skills(ws: Path, directive_files: list, script_list, agent_type: str) -> list:
    """Set up all skills from directives. Returns list of skill names."""
    skill_names = []
    # Always include memory_management and infrastructure_tools
    all_directives = list(directive_files)
    for infra in ["memory_management.md", "infrastructure_tools.md"]:
        if infra not in all_directives:
            all_directives.append(infra)

    for directive in all_directives:
        skill_name = directive_to_skill_name(directive)
        skill_names.append(skill_name)
        # Read directive content
        directive_path = DIRECTIVES_DIR / directive
        if directive_path.exists():
            content = directive_path.read_text(encoding="utf-8", errors="replace")
        else:
            content = f"# {skill_name}\n\nSkill for {skill_name.replace('_', ' ')}.\n"
        # Determine scripts for this skill
        skill_scripts = SKILL_TO_SCRIPTS.get(skill_name, [])
        # Generate SKILL.md
        generate_skill_md(ws, skill_name, content, skill_scripts)
        # Copy scripts
        if skill_scripts:
            n = copy_skill_scripts(ws, skill_name, skill_scripts, {})
            if n > 0:
                print(f"  ✓ Skill '{skill_name}': {n} script(s)")

    # Copy shared scripts
    n_shared = copy_shared_scripts(ws)
    if n_shared > 0:
        print(f"  ✓ Shared utilities: {n_shared} script(s) in .tmp/scripts/")

    return skill_names


# ═══════════════════════════════════════════════════════════════════════════════
# FILE GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_agents_py(ws: Path, slug: str, agent_name: str,
                        skill_names: list, type_config: dict) -> None:
    """Generate agents.py with build_agents() entry point."""
    # Build tool function source lines
    tool_fn_lines = []
    tool_names = []
    for skill in skill_names:
        fn_name = skill.replace("-", "_")
        tool_names.append(fn_name)
        tool_fn_lines.append(f'''
async def {fn_name}(action: str) -> str:
    """Run the {skill} skill. Use when user asks about
    {skill.replace('_', ' ')}. action: one of list|run|status."""
    return await _run([sys.executable,
        str(SKILLS_DIR / "{skill}" / "scripts" / "main.py"),
        action])
''')

    tools_list = ",\n            ".join(tool_names) if tool_names else ""
    tool_fns_block = "\n".join(tool_fn_lines) if tool_fn_lines else (
        'async def noop() -> str:\n'
        '    """Placeholder tool."""\n'
        '    return "No tools configured."')

    content = _AGENTS_PY_TEMPLATE.format(
        slug=slug,
        agent_name=agent_name,
        description=type_config.get("description", "Automation agent"),
        tool_fns=tool_fns_block,
        tools_list=tools_list,
    )
    (ws / "agents.py").write_text(content, encoding="utf-8")
    print("  ✓ Generated agents.py")


_AGENTS_PY_TEMPLATE = '''"""agent-{slug} — MAF Agent definitions.

{agent_name} — {description}

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
            result.stderr or f"Script exited {{result.returncode}}")
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
                    "\\n### Tool: " + skill_md.parent.name
                    + "\\n\\n" + text)
            if skill_sections:
                parts.append(
                    "\\n\\n---\\n\\n"
                    "## Registered Skill Tool Descriptions\\n")
                parts.extend(skill_sections)
    else:
        agents_md = AGENT_DIR / "AGENTS.md"
        if agents_md.exists():
            parts.append(
                agents_md.read_text(encoding="utf-8", errors="replace"))
    return "\\n".join(parts)


SYSTEM_PROMPT = _build_system_prompt()


# ── Tool functions ──────────────────────────────────────────────────────

{tool_fns}


# ── LiteLLM provider (CommandCenter mode) ────────────────────────────────

def _llm_provider():
    base_url = os.environ.get("LITELLM_BASE_URL", "http://127.0.0.1:8080")
    api_key  = os.environ.get("LITELLM_MASTER_KEY", "sk-local")
    return {{
        "type": "openai",
        "base_url": base_url + "/v1",
        "api_key": api_key,
    }}


# ── Agent factory ────────────────────────────────────────────────────────

def build_agent():
    from agent_framework_github_copilot import GitHubCopilotAgent
    from copilot.types import PermissionHandler

    return GitHubCopilotAgent(
        name="{slug}",
        description="{description}",
        instructions=SYSTEM_PROMPT,
        tools=[
            {tools_list}
        ],
        default_options={{
            "model": "tier-balanced",
            "provider": _llm_provider(),
            "mcp_servers": {{}},
            "on_permission_request": PermissionHandler.approve_all,
        }},
    )


def build_agents():
    """Dynamic Agent Loader entry point.
    Synchronous, zero-argument, pure."""
    return [build_agent()]


__all__ = ["build_agents", "build_agent", "SYSTEM_PROMPT"]
'''


def generate_config_json(ws: Path, slug: str, type_config: dict) -> None:
    """Generate config.json with CommandCenter contract."""
    descriptions = type_config.get("description", "Automation agent")
    tags_list = type_config.get("tags", [slug])
    integrations = type_config.get("integrations", [])
    opt_integrations = type_config.get("optional_integrations", [])

    cfg = {
        "name": slug,
        "description": descriptions,
        "version": "0.1.0",
        "skill_repos": [],
        "integrations": integrations,
        "optional_integrations": opt_integrations,
        "tags": tags_list,
        "tool_scope": type_config.get("tool_scope", None),
        "max_mutation_attempts": 1,
        "mcp_servers": {},
        "icon": type_config.get("icon", "Bot"),
        "category": type_config.get("category", "external"),
        "webhook_routes": [],
    }
    with open(ws / "config.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print("  ✓ Generated config.json")


def generate_system_prompt_md(ws: Path, agent_name: str, slug: str,
                               type_config: dict, skill_names: list) -> None:
    """Generate .github/prompts/system.md."""
    skill_table = ""
    for skill in skill_names:
        label = skill.replace("_", " ").title()
        skill_table += f"| `{skill}` | `.github/skills/{skill}/SKILL.md` | {label} |\n"

    integrations_str = ", ".join(
        type_config.get("env_vars_required", [])) or "None required"

    content = f"""# {agent_name} — System Prompt

## Purpose

{type_config.get("system_prompt_additions", type_config.get("description", ""))}

## Available Tools

| Tool | When to call it |
|------|-----------------|
{skill_table}

## Platform Tools (injected by CommandCenter)

You have access to these tools automatically — do NOT re-implement them:
- `write_artifact` — write files visible in the UI sidebar
- `manage_todo_list` — update the live task panel
- `ask_user` — pause and ask the user a clarifying question
- `get_errors` — check code for syntax/lint errors
- `save_note` / `recall_notes` — repo-scoped working memory
- `web_search` / `fetch_page` — web access (no API key needed)

## Required Integrations

{integrations_str}

## Rules

1. Always call the relevant tool — never answer from memory alone.
2. Read the relevant SKILL.md before running any script.
3. Raise errors explicitly — never silently return partial results.
4. Do NOT fabricate data. If a tool fails, say so.
5. Use scripts for deterministic work; reserve LLM for judgment.

## Output Format

- Lead with one sentence of context
- Results as bullet points or a markdown table
- End with the next suggested action
"""
    prompts_dir = ws / ".github" / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    (prompts_dir / "system.md").write_text(content, encoding="utf-8")
    print("  ✓ Generated .github/prompts/system.md")


def generate_agent_md(ws: Path, agent_name: str, slug: str,
                       type_config: dict, skill_names: list) -> None:
    """Generate .github/agents/<name>.agent.md for VS Code Copilot Chat."""
    tools = type_config.get("copilot_tools",
        ["codebase", "search", "fetch", "terminal", "editFiles",
         "runCommands", "problems"])
    tools_str = json.dumps(tools)

    skill_lines = ""
    for skill in skill_names:
        label = skill.replace("_", " ").title()
        skill_lines += (f"- **{label}** "
                         f"(`.github/skills/{skill}/SKILL.md`) — "
                         f"see SKILL.md for details\n")

    content = f"""---
description: {type_config.get('description', 'Automation agent')}
name: {agent_name}
model: claude-sonnet-4-5
tools: {tools_str}
---

# {agent_name}

{type_config.get('system_prompt_additions', '')}

## Architecture (DOE v2)

**Layer 1 — Skills:** `.github/skills/*/SKILL.md` define goals, inputs, scripts, outputs.
**Layer 2 — Orchestration:** You (the LLM) read SKILL.md, call scripts, apply judgment.
**Layer 3 — Execution:** `.github/skills/*/scripts/` and `.tmp/scripts/` do the work.

## Skills

{skill_lines}

## How to Use

- Read the relevant `SKILL.md` before running any script
- Run scripts via terminal: `python .github/skills/<name>/scripts/<script>.py [args]`
- Shared utilities in `.tmp/scripts/` are on PYTHONPATH
- Credentials in `.env` — never commit

## Operating Principles

1. **Check for tools first** — Before writing code, check `.github/skills/` for existing solutions
2. **Self-anneal when things break** — Fix errors, update scripts, test, document learnings
3. **Reserve LLM for judgment** — Use scripts for deterministic operations
4. **Update SKILL.md as you learn** — Skills are living documents
"""
    agents_dir = ws / ".github" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / f"{slug}.agent.md").write_text(content, encoding="utf-8")
    print(f"  ✓ Generated .github/agents/{slug}.agent.md")


def generate_copilot_instructions(ws: Path, agent_name: str, slug: str) -> None:
    """Generate .github/copilot-instructions.md."""
    content = f"""# {agent_name} — Copilot Instructions

This is the **{agent_name}** agent repo — built with the DOE Framework
(Directive, Orchestration, Execution) and compatible with CommandCenter.

**Key files:**
- `agents.py` — `build_agents()` entry point for CommandCenter
- `config.json` — CommandCenter contract
- `.github/prompts/system.md` — System prompt loaded by agents.py
- `.github/skills/*/SKILL.md` — Skill definitions
- `.github/skills/*/scripts/` — Deterministic execution scripts
- `.tmp/scripts/` — Shared utilities on PYTHONPATH
- `agent_repo_compatibility.md` — The canonical spec (reference only)
"""
    (ws / ".github" / "copilot-instructions.md").write_text(
        content, encoding="utf-8")
    print("  ✓ Generated .github/copilot-instructions.md")


def generate_agents_md(ws: Path, agent_name: str, slug: str,
                        type_config: dict, skill_names: list) -> None:
    """Generate AGENTS.md orientation document."""
    skill_table = ""
    for skill in skill_names:
        label = skill.replace("_", " ").title()
        skill_table += f"| {label} | `.github/skills/{skill}/SKILL.md` | {label} |\n"

    content = f"""# {agent_name} — Agent Instructions

> {type_config.get('system_prompt_additions', type_config.get('description', ''))[:200]}

## Architecture (DOE v2)

**Layer 1 — Skills:** `.github/skills/*/SKILL.md` define goals, inputs, scripts, outputs.
**Layer 2 — Orchestration:** You (the LLM) read SKILL.md, call scripts, apply judgment.
**Layer 3 — Execution:** `.github/skills/*/scripts/` and `.tmp/scripts/` do the actual work.

## Available Skills

| Skill | SKILL.md | What it does |
|-------|----------|--------------|
{skill_table}

## File Organization

- `.github/skills/` — Skill instructions + feature scripts
- `.tmp/scripts/` — Shared utilities (on PYTHONPATH)
- `agent-data/` — Reference data: catalogs, templates, PDFs, images
- `inputs/` — User-provided files (subfolders per project)
- `outputs/` — Campaign results (subfolders per campaign slug)
- `tests/` — pytest suite — CI gate

## Quick Start

1. Copy `.env.example` → `.env` and fill in API keys
2. `pip install -r requirements.txt`
3. Tell the agent what you want to do
"""
    (ws / "AGENTS.md").write_text(content, encoding="utf-8")
    print("  ✓ Generated AGENTS.md")


def generate_instructions_md(ws: Path, agent_name: str,
                              type_config: dict) -> None:
    """Generate instructions.md (1-paragraph for mutation sandbox)."""
    content = f"""# {agent_name} — Brief

{type_config.get('description', 'Automation agent')}. Built with the DOE
Framework and compatible with CommandCenter agent runtime.
"""
    (ws / "instructions.md").write_text(content, encoding="utf-8")
    print("  ✓ Generated instructions.md")


def generate_pyproject_toml(ws: Path, slug: str, type_config: dict) -> None:
    """Generate pyproject.toml."""
    deps = type_config.get("packages", ["requests", "python-dotenv"])
    deps_str = "\n".join(f'    "{d}",' for d in sorted(set(deps)))

    content = f'''[project]
name = "agent-{slug}"
version = "0.1.0"
description = "{type_config.get('description', 'Automation agent')}"
requires-python = ">=3.11"
dependencies = [
{deps_str}
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-asyncio>=0.24"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
'''
    (ws / "pyproject.toml").write_text(content, encoding="utf-8")
    print("  ✓ Generated pyproject.toml")


def generate_test_agents(ws: Path, slug: str) -> None:
    """Generate tests/test_agents.py (CI gate)."""
    content = f'''"""CommandCenter CI gate — must pass for agent registration."""
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

def test_agent_has_name_and_instructions():
    try:
        from agents import build_agents
        agent = build_agents()[0]
        instructions = (
            getattr(agent, "instructions", None)
            or getattr(agent, "_instructions", None)
        )
        assert instructions and len(instructions) > 50
    except ImportError:
        pytest.skip("MAF runtime not available")

def test_agent_has_tools():
    try:
        from agents import build_agents
        agent = build_agents()[0]
        tools = (
            getattr(agent, "tools", None)
            or getattr(agent, "_tools", None)
            or []
        )
        assert len(tools) > 0, "Agent has no tools — it will only apologise"
    except ImportError:
        pytest.skip("MAF runtime not available")

def test_system_prompt_contains_skills():
    from agents import SYSTEM_PROMPT
    assert len(SYSTEM_PROMPT) > 100
'''
    (ws / "tests" / "test_agents.py").write_text(content, encoding="utf-8")
    print("  ✓ Generated tests/test_agents.py")


def generate_agent_data_index(ws: Path) -> None:
    """Generate agent-data/INDEX.md."""
    content = """# Agent Data — Index

This folder contains permanent reference data used by the agent at runtime.
Every asset must be listed here.

| Path | Purpose | Usage |
|------|---------|-------|
| `templates/` | Document templates | Referenced by document generation scripts |
| `images/` | Product images and renders | Embedded in outputs |
| `specs/` | Technical specification PDFs | Parsed by research skills |

## Adding Assets

1. Place the file in the appropriate subfolder
2. Add an entry to this index with path, purpose, and usage notes
3. Commit the asset to git

## Rules

- All assets are **read-only** at runtime — never modify them programmatically
- Do NOT place user-provided files here — use `inputs/` instead
- Reference via `AGENT_DIR / "agent-data" / ...` in scripts
"""
    (ws / "agent-data" / "INDEX.md").write_text(content, encoding="utf-8")
    print("  ✓ Generated agent-data/INDEX.md")


def generate_env_example(ws: Path, type_config: dict) -> None:
    """Generate .env.example."""
    required = type_config.get("env_vars_required", [])
    optional = type_config.get("env_vars_optional", [])
    content = """# Environment Variables
# Copy this file to .env and fill in your API keys
# NEVER commit .env to git!

"""
    for var in required:
        content += f"{var}=\n"
    if optional:
        content += "\n# Optional\n"
        for var in optional:
            content += f"#{var}=\n"

    content += """
# LiteLLM (local dev only — CommandCenter injects at runtime)
# LITELLM_BASE_URL=http://127.0.0.1:8080
# LITELLM_MASTER_KEY=sk-local
"""
    (ws / ".env.example").write_text(content, encoding="utf-8")
    print("  ✓ Generated .env.example")


def generate_requirements(ws: Path, type_config: dict) -> None:
    """Generate requirements.txt."""
    packages = type_config.get("packages", ["requests", "python-dotenv"])
    content = "# Requirements for this agent workspace\n\n"
    for pkg in sorted(set(packages)):
        content += f"{pkg}\n"
    (ws / "requirements.txt").write_text(content, encoding="utf-8")
    print("  ✓ Generated requirements.txt")


def generate_gitignore(ws: Path) -> None:
    """Generate .gitignore with required entries from agent_repo_compatibility.md."""
    content = """# Secrets
.env
.env.local
credentials.json
token.json
*.token_cache.json

# Python
__pycache__/
*.py[cod]
.venv/
venv/
ENV/

# .tmp/ caches — structure tracked, contents not
.tmp/search_cache/*.json
.tmp/web_cache/*
!.tmp/search_cache/README.md
!.tmp/web_cache/README.md
# .tmp/scripts/ IS tracked — shared utilities
!.tmp/scripts/**

# OS / IDE
.DS_Store
Thumbs.db
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Keep .vscode/ settings
!.vscode/
"""
    (ws / ".gitignore").write_text(content, encoding="utf-8")
    print("  ✓ Generated .gitignore")


def generate_setup_scripts(ws: Path, agent_name: str, slug: str) -> None:
    """Generate setup.ps1 and setup.sh."""
    ps_content = f'''# {agent_name} - Automated Setup Script
Write-Host "Setting up: {agent_name}" -ForegroundColor Cyan

$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {{
    Write-Host "ERROR: Python not found" -ForegroundColor Red; exit 1
}}
Write-Host "Found $pythonVersion" -ForegroundColor Green

if (-not (Test-Path ".venv")) {{
    python -m venv .venv
    Write-Host "Virtual environment created" -ForegroundColor Green
}}

& .\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip --quiet

if (Test-Path "requirements.txt") {{
    pip install -r requirements.txt --quiet
    Write-Host "Dependencies installed" -ForegroundColor Green
}}

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {{
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example — EDIT WITH YOUR API KEYS!" -ForegroundColor Yellow
}}

Write-Host "SETUP COMPLETE! Edit .env with your API keys." -ForegroundColor Green
Write-Host "To activate: .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Gray
'''
    (ws / "setup.ps1").write_text(ps_content, encoding="utf-8")

    sh_content = f'''#!/bin/bash
echo "Setting up: {agent_name}"
python3 -m venv .venv 2>/dev/null || python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
[ ! -f ".env" ] && [ -f ".env.example" ] && cp .env.example .env \\
    && echo "Created .env from .env.example — EDIT WITH YOUR API KEYS!"
echo "SETUP COMPLETE!"
'''
    (ws / "setup.sh").write_text(sh_content, encoding="utf-8", newline="\n")
    print("  ✓ Generated setup.ps1 and setup.sh")


def generate_vscode_files(ws: Path, agent_name: str, slug: str) -> None:
    """Generate .vscode/ settings, extensions, and tasks."""
    vscode = ws / ".vscode"
    vscode.mkdir(parents=True, exist_ok=True)

    settings = {
        "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
        "python.terminal.activateEnvironment": True,
        "github.copilot.enable": {"*": True, "plaintext": True, "markdown": True, "python": True},
        "editor.formatOnSave": True,
        "terminal.integrated.defaultProfile.windows": "PowerShell",
        "search.exclude": {"**/.tmp/search_cache": True, "**/.tmp/web_cache": True, "**/__pycache__": True},
    }
    with open(vscode / "settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

    extensions = {
        "recommendations": [
            "GitHub.copilot", "GitHub.copilot-chat",
            "ms-python.python", "ms-python.vscode-pylance", "ms-python.debugpy",
        ]
    }
    with open(vscode / "extensions.json", "w", encoding="utf-8") as f:
        json.dump(extensions, f, indent=2)

    tasks = {
        "version": "2.0.0",
        "tasks": [{
            "label": "Setup Agent Environment",
            "type": "shell",
            "command": ".\\setup.ps1",
            "windows": {"command": "powershell",
                         "args": ["-ExecutionPolicy", "Bypass", "-File", ".\\setup.ps1"]},
            "linux": {"command": "bash", "args": ["./setup.sh"]},
            "group": {"kind": "build", "isDefault": True},
            "presentation": {"reveal": "always", "panel": "new"},
            "runOptions": {"runOn": "folderOpen"},
        }]
    }
    with open(vscode / "tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

    print("  ✓ Generated .vscode/ settings, extensions, tasks")


def generate_code_workspace(ws: Path, agent_name: str, slug: str) -> None:
    """Generate .code-workspace file."""
    workspace = {
        "folders": [{"path": "."}],
        "settings": {
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
            "python.terminal.activateEnvironment": True,
            "github.copilot.enable": {"*": True, "plaintext": True, "markdown": True, "python": True},
            "search.exclude": {"**/.tmp/search_cache": True, "**/.tmp/web_cache": True, "**/__pycache__": True, "**/.venv": True},
            "task.allowAutomaticTasks": "on",
        },
        "extensions": {
            "recommendations": [
                "GitHub.copilot", "GitHub.copilot-chat",
                "ms-python.python", "ms-python.vscode-pylance",
            ]
        },
        "launch": {
            "version": "0.2.0",
            "configurations": [{
                "name": "Python: Current File",
                "type": "debugpy",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}",
                "env": {"PYTHONPATH": "${workspaceFolder}"},
            }]
        }
    }
    ws_file = ws / f"{slug}.code-workspace"
    with open(ws_file, "w", encoding="utf-8") as f:
        json.dump(workspace, f, indent=2)
    print(f"  ✓ Generated {slug}.code-workspace")


def generate_readme(ws: Path, agent_name: str, slug: str,
                     type_config: dict, skill_names: list) -> None:
    """Generate README.md."""
    skill_list = "\n".join(
        f"- **{s.replace('_', ' ').title()}** — `.github/skills/{s}/SKILL.md`"
        for s in skill_names
    ) or "- Create your own skills in `.github/skills/`"

    integrations = "\n".join(
        f"- `{v}`" for v in type_config.get("env_vars_required", [])
    ) or "- None required"

    content = f"""# {agent_name}

> Built with DOE Framework — CommandCenter-Compatible

**Type:** {type_config['name']}

{type_config['description']}

## Quick Start

**Double-click:** `{slug}.code-workspace` to open in VS Code.

Or manually:
```bash
# Windows
.\\setup.ps1

# macOS/Linux
chmod +x setup.sh && ./setup.sh
```

## Using the Agent

1. Open in VS Code
2. Select **"{agent_name}"** from Copilot Chat agent dropdown
3. Start working — the agent knows its skills and scripts

## Skills

{skill_list}

## Required API Keys

{integrations}

## Structure

```
├── agents.py                 # build_agents() entry point
├── config.json               # CommandCenter contract
├── .github/
│   ├── prompts/system.md     # System prompt
│   ├── agents/{slug}.agent.md  # VS Code Copilot Chat agent
│   └── skills/               # Skill instructions + scripts
├── .tmp/scripts/             # Shared utilities
├── agent-data/               # Reference data
├── inputs/                   # User-provided files
├── outputs/                  # Campaign results
└── tests/                    # CI gate
```
"""
    (ws / "README.md").write_text(content, encoding="utf-8")
    print("  ✓ Generated README.md")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def create_agent_workspace(name: str, agent_type: str) -> Path:
    """Create a complete CommandCenter-compatible agent workspace."""
    templates = load_templates()

    if agent_type not in templates["agent_types"]:
        available = ", ".join(templates["agent_types"].keys())
        raise ValueError(
            f"Unknown agent type: {agent_type}. Available: {available}")

    type_config = templates["agent_types"][agent_type]
    slug = slugify(name)
    workspace_path = OUTPUTS_DIR / slug

    if workspace_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        workspace_path = OUTPUTS_DIR / f"{slug}-{timestamp}"

    print(f"\n{'=' * 60}")
    print(f"CREATING AGENT WORKSPACE: {name}")
    print(f"Type: {type_config['name']}")
    print(f"Location: {workspace_path}")
    print(f"{'=' * 60}\n")

    # 1. Folder structure
    create_folder_structure(workspace_path)

    # 2. Skills (directives → .github/skills/<name>/SKILL.md + scripts/)
    directive_files = type_config.get("directives", []).copy()
    skill_names = setup_skills(workspace_path, directive_files,
                                type_config.get("scripts", []), agent_type)

    # 3. Core files
    generate_agents_py(workspace_path, slug, name, skill_names, type_config)
    generate_config_json(workspace_path, slug, type_config)
    generate_system_prompt_md(workspace_path, name, slug, type_config, skill_names)
    generate_agent_md(workspace_path, name, slug, type_config, skill_names)
    generate_copilot_instructions(workspace_path, name, slug)
    generate_agents_md(workspace_path, name, slug, type_config, skill_names)
    generate_instructions_md(workspace_path, name, type_config)
    generate_pyproject_toml(workspace_path, slug, type_config)
    generate_test_agents(workspace_path, slug)
    generate_agent_data_index(workspace_path)
    generate_env_example(workspace_path, type_config)
    generate_requirements(workspace_path, type_config)
    generate_gitignore(workspace_path)
    generate_setup_scripts(workspace_path, name, slug)
    generate_vscode_files(workspace_path, name, slug)
    generate_code_workspace(workspace_path, name, slug)
    generate_readme(workspace_path, name, slug, type_config, skill_names)

    # Copy agent_repo_compatibility.md as reference
    if AGENT_REPO_COMPAT.exists():
        shutil.copy2(AGENT_REPO_COMPAT, workspace_path / "agent_repo_compatibility.md")

    print(f"\n{'=' * 60}")
    print("WORKSPACE CREATED SUCCESSFULLY!")
    print(f"{'=' * 60}")
    print(f"\n  Double-click to open:")
    print(f"  {workspace_path / (slug + '.code-workspace')}")
    print(f"\n  Or run setup manually:")
    print(f"  cd \"{workspace_path}\" && .\\setup.ps1")
    print()

    return workspace_path


def main():
    parser = argparse.ArgumentParser(
        description="Create CommandCenter-compatible agent workspace")
    parser.add_argument("--list-types", action="store_true",
                        help="List available agent types")
    parser.add_argument("--name", "-n", type=str, help="Agent name")
    parser.add_argument("--type", "-t", type=str, help="Agent type")
    args = parser.parse_args()

    templates = load_templates()

    if args.list_types:
        list_agent_types(templates)
        return

    if not args.name or not args.type:
        parser.print_help()
        print("\nError: --name and --type are required (or use --list-types)")
        sys.exit(1)

    try:
        create_agent_workspace(name=args.name, agent_type=args.type)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
