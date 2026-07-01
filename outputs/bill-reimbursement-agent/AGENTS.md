# Bill Reimbursement Agent — Agent Instructions

> You are a custom automation agent. Your capabilities will be defined by the directives and scripts added to this workspace.

## Architecture (DOE v2)

**Layer 1 — Skills:** `.github/skills/*/SKILL.md` define goals, inputs, scripts, outputs.
**Layer 2 — Orchestration:** You (the LLM) read SKILL.md, call scripts, apply judgment.
**Layer 3 — Execution:** `.github/skills/*/scripts/` and `.tmp/scripts/` do the actual work.

## Available Skills

| Skill | SKILL.md | What it does |
|-------|----------|--------------|
| Memory Management | `.github/skills/memory_management/SKILL.md` | Memory Management |
| Infrastructure Tools | `.github/skills/infrastructure_tools/SKILL.md` | Infrastructure Tools |


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
