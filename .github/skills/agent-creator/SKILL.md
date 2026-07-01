---
name: agent-creator
description: >
  Create new CommandCenter-compatible agent workspaces from templates.
  Use when the user asks to create, build, scaffold, or generate a new
  automation agent. Supports multiple agent types including lead_gen,
  email, proposals, video, CRM, business planning, research, legal,
  HR, PR, and custom.
when_to_use: "User asks to create/build/scaffold/generate a new agent workspace."
authority: write
cost_tier: 1
version: 0.1.0
---

# Agent Creator Skill

Creates complete, production-ready agent workspaces that comply with CommandCenter
agent-repo compatibility standards. Every generated workspace includes `agents.py`,
`config.json`, `.github/prompts/system.md`, `.github/skills/`, `.tmp/scripts/`,
`agent-data/`, `tests/`, and all required configuration files.

## Scripts

| Script                    | Purpose                                       |
| ------------------------- | --------------------------------------------- |
| `scripts/create_workspace.py` | Primary entry point — creates a new workspace |
| `scripts/upgrade_agent.py`    | Upgrades existing agent to latest standards   |
| `scripts/validate_agent.py`   | Validates agent against compatibility rules   |

## Usage

```bash
# Create a new agent
python .github/skills/agent-creator/scripts/create_workspace.py --name "My Agent" --type lead_generation

# List available types
python .github/skills/agent-creator/scripts/create_workspace.py --list-types

# Upgrade an existing agent
python .github/skills/agent-creator/scripts/upgrade_agent.py --path /path/to/agent

# Validate an agent
python .github/skills/agent-creator/scripts/validate_agent.py --path /path/to/agent
```

## Required Environment Variables

- None required. The agent creator works entirely with local files.
  Optional: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` for standalone mode.

## Outputs

Creates a new agent workspace in `outputs/<agent-slug>/` with the full
CommandCenter-compatible structure ready for immediate use.
