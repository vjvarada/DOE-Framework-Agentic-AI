# Bill Reimbursement Agent

> Built with DOE Framework — CommandCenter-Compatible

**Type:** Custom Agent

Minimal base setup - add your own directives and scripts

## Quick Start

**Double-click:** `bill-reimbursement-agent.code-workspace` to open in VS Code.

Or manually:
```bash
# Windows
.\setup.ps1

# macOS/Linux
chmod +x setup.sh && ./setup.sh
```

## Using the Agent

1. Open in VS Code
2. Select **"Bill Reimbursement Agent"** from Copilot Chat agent dropdown
3. Start working — the agent knows its skills and scripts

## Skills

- **Memory Management** — `.github/skills/memory_management/SKILL.md`
- **Infrastructure Tools** — `.github/skills/infrastructure_tools/SKILL.md`

## Required API Keys

- `GOOGLE_SHEETS_CREDENTIALS_FILE`

## Structure

```
├── agents.py                 # build_agents() entry point
├── config.json               # CommandCenter contract
├── .github/
│   ├── prompts/system.md     # System prompt
│   ├── agents/bill-reimbursement-agent.agent.md  # VS Code Copilot Chat agent
│   └── skills/               # Skill instructions + scripts
├── .tmp/scripts/             # Shared utilities
├── agent-data/               # Reference data
├── inputs/                   # User-provided files
├── outputs/                  # Campaign results
└── tests/                    # CI gate
```
