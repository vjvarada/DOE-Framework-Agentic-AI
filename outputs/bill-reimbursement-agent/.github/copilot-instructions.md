# Bill Reimbursement Agent — Copilot Instructions

This is the **Bill Reimbursement Agent** agent repo — built with the DOE Framework
(Directive, Orchestration, Execution) and compatible with CommandCenter.

**Key files:**
- `agents.py` — `build_agents()` entry point for CommandCenter
- `config.json` — CommandCenter contract
- `.github/prompts/system.md` — System prompt loaded by agents.py
- `.github/skills/*/SKILL.md` — Skill definitions
- `.github/skills/*/scripts/` — Deterministic execution scripts
- `.tmp/scripts/` — Shared utilities on PYTHONPATH
- `agent_repo_compatibility.md` — The canonical spec (reference only)
