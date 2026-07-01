# Agent Creator — Copilot Instructions

This is the **Agent Creator** repo — it builds production-ready, CommandCenter-compatible
agent workspaces using the DOE Framework (Directive, Orchestration, Execution).

**Key files:**
- `agents.py` — `build_agents()` entry point for CommandCenter dynamic agent loading
- `config.json` — CommandCenter contract (name, integrations, tags, tool_scope)
- `.github/prompts/system.md` — System prompt loaded by agents.py at runtime
- `.github/skills/agent-creator/SKILL.md` — Skill definition for workspace creation
- `.github/skills/agent-creator/scripts/create_workspace.py` — Main workspace generator
- `agent_repo_compatibility.md` — The canonical spec all generated agents must follow

**Architecture:** Skills (what to do) → Orchestration (decision making) → Execution (doing the work)
