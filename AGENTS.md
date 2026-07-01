# Agent Creator — Agent Instructions

> Expert agent that creates other agents using the DOE Framework.
> Builds complete, production-ready agent workspaces with skills, scripts,
> and automated setup — fully CommandCenter-compatible.

## Architecture (DOE v2)

**Layer 1 — Skills:** `.github/skills/*/SKILL.md` define goals, inputs, scripts, outputs.
**Layer 2 — Orchestration:** You (the LLM) read SKILL.md, call scripts, apply judgment.
**Layer 3 — Execution:** `.github/skills/*/scripts/` and `.tmp/scripts/` do the actual work.

## Available Skills

| Skill | SKILL.md | What it does |
|-------|----------|--------------|
| Agent Creator | `.github/skills/agent-creator/SKILL.md` | Create, upgrade, and validate agent workspaces |

## Platform Tools (injected by CommandCenter)

- `write_artifact` — write files visible in the UI sidebar
- `manage_todo_list` — update the live task panel
- `ask_user` — pause and ask the user a clarifying question
- `get_errors` — check code for syntax/lint errors
- `save_note` / `recall_notes` — repo-scoped working memory
- `web_search` / `fetch_page` — web access (no API key needed)

## File Organization

- `.github/skills/` — Skill instructions + feature scripts
- `.tmp/scripts/` — Shared utilities (on PYTHONPATH)
- `agent-data/` — Reference data: catalogs, templates, PDFs, images
- `inputs/` — User-provided files (subfolders per project)
- `outputs/` — Campaign results and generated agent workspaces
- `tests/` — pytest suite — CI gate
- `directives/` — Original SOPs (source for skills)
- `execution/` — Original scripts (source for skill scripts)

## Quick Start

1. Copy `.env.example` → `.env` and fill in API keys (optional)
2. `pip install -r requirements.txt`
3. Tell the agent what kind of agent you want to create

## Self-annealing loop

Errors are learning opportunities. When something breaks:
1. Fix it
2. Update the tool
3. Test tool, make sure it works
4. Update directive to include new flow
5. **Store the lesson in memory** (`add-insight`, `add-fact`)
6. System is now stronger

## Memory System

Every agent has a local SQLite database (`memory/agent_memory.db`) with full-text search (FTS5). This provides persistent context across sessions.

**Dual-Memory Architecture:**
- **Short-Term Memory (STM)** — Session/task working memory with optional TTL (auto-expires)
- **Long-Term Memory (LTM)** — Persistent facts, entities, insights, decisions, interactions

**Key commands:**
```bash
python execution/memory_db.py search "<keywords>"          # Search all memory
python execution/memory_db.py stm set "key" "value"         # Set session state
python execution/memory_db.py add-fact "<fact>" --category x # Store knowledge
python execution/memory_db.py add-insight "<lesson>"        # Store lesson learned
python execution/memory_db.py status                        # Check memory health
```

**Advanced features:**
```bash
python execution/memory_db.py hybrid-search "query"        # BM25 + semantic search (needs sentence-transformers)
python execution/memory_db.py embed-sync                    # Build embeddings for semantic search
python execution/memory_db.py consolidate-stm               # Promote valuable STM to facts
python execution/memory_db.py deduplicate-facts             # Remove duplicates
python execution/memory_db.py reflect --json                # Consolidation report
python execution/memory_db.py check-guardrails --task X --output-text "..."  # Validate output
python execution/memory_db.py log-eval --task X --status success --cost 0.05 # Track evaluations
python execution/memory_db.py eval-summary --days 7         # Cost/quality dashboard
```

For full protocol, see `directives/memory_management.md`.

## Tool Registry

Every execution script has a formal schema in `execution/tool_registry.json`. Use it for structured tool discovery.

**Key commands:**
```bash
python execution/tool_registry.py list                   # List all tools by category
python execution/tool_registry.py show <tool_name>       # Full schema for a tool
python execution/tool_registry.py find "<query>"         # Search tools by keyword
python execution/tool_registry.py validate               # Check scripts exist & env vars set
python execution/tool_registry.py schema <tool_name>     # Get OpenAI function-call schema
```

**Before any task**, run `find` to discover relevant tools and `show` to get parameter schemas.

## Task Graphs (Execution Plans)

Multi-step workflows run as DAGs with dependency resolution, checkpointing, and resume-from-failure.

**Key commands:**
```bash
python execution/task_graph.py create "Pipeline" --step "scrape:Scrape" --step "enrich:Enrich:scrape"
python execution/task_graph.py show <plan_id>            # Visual status of all steps
python execution/task_graph.py ready <plan_id>           # Steps ready to execute
python execution/task_graph.py mark <plan_id> <step> completed --output "Result"
python execution/task_graph.py reset <plan_id> <step>    # Reset step + downstream
```

## Human-in-the-Loop (Approval Gates)

Approval gates for irreversible actions. Tools with `requires_confirmation: true` in the registry must get approval before execution.

**Key commands:**
```bash
python execution/confirm_action.py request "Action description" --tool <name> --risk high
python execution/confirm_action.py approve <id> --reason "Approved"
python execution/confirm_action.py deny <id> --reason "Too expensive"
python execution/confirm_action.py list-pending
```

Set `AGENT_AUTO_APPROVE=true` for testing/CI only.

## Execution Traces (Observability)

Structured trace logging for every tool call. Tracks timing, costs, tokens, and errors.

**Key commands:**
```bash
python execution/execution_trace.py start "Trace Name" --plan <plan_id>
python execution/execution_trace.py log <trace_id> --tool <name> --status success --duration 12.5
python execution/execution_trace.py end <trace_id> --status success
python execution/execution_trace.py show <trace_id>      # Visual timeline
python execution/execution_trace.py stats --days 7       # Aggregate dashboard
```

**Programmatic use:**
```python
from execution_trace import Tracer
with Tracer("Pipeline") as t:
    t.log_step("step1", tool="scrape_google_maps", duration_s=12.5, cost_usd=0.01)
# Auto-ends, auto-catches errors
```

For full details, see `directives/infrastructure_tools.md`.

## File Organization

**Deliverables vs Intermediates:**
- **Deliverables**: Google Sheets, Google Slides, or other cloud-based outputs that the user can access
- **Intermediates**: Temporary files needed during processing

**Directory structure:**
- `.tmp/` - All intermediate files (dossiers, scraped data, temp exports). Never commit, always regenerated.
- `memory/` - SQLite database and memory files. Persistent across sessions.
- `execution/` - Python scripts (the deterministic tools)
- `directives/` - SOPs in Markdown (the instruction set)
- `.env` - Environment variables and API keys
- `credentials.json`, `token.json` - Google OAuth credentials (required files, in `.gitignore`)

**Key principle:** Local files are only for processing. Deliverables live in cloud services (Google Sheets, Slides, etc.) where the user can access them. Everything in `.tmp/` can be deleted and regenerated.

## Summary

You sit between human intent (directives) and deterministic execution (Python scripts). Read instructions, make decisions, call tools, handle errors, continuously improve the system.

Be pragmatic. Be reliable. Self-anneal.
