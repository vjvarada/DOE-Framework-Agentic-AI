# Memory Management Directive

## Purpose
Manage persistent memory across sessions so the agent gets smarter over time. Memory is the agent's competitive advantage over generic AI chat — it enables continuity, learning, and personalization.

## Architecture: Dual-Memory System

### Short-Term Memory (STM)
Working memory for the current session/task. Auto-expires. Use for:
- Current task state and progress
- Temporary variables (last error, current batch #, retry count)
- In-flight data that doesn't need to persist

### Long-Term Memory (LTM)  
Persistent knowledge that survives across sessions. Use for:
- **Facts** — Atomic pieces of knowledge (API limits, preferences, constraints)
- **Entities** — People, companies, tools, concepts the agent interacts with
- **Insights** — Lessons learned, patterns discovered (append-only, never delete)
- **Decisions** — Choices made with reasoning and outcomes
- **Interactions** — Log of past conversations and tasks completed
- **Context** — Mutable current state (project stage, client info)
- **Profile** — Static identity info (agent type, project details)

## Tool: execution/memory_db.py

### Universal Search (Primary Interface)
`ash
python execution/memory_db.py search "rate limit API"
python execution/memory_db.py search "client preferences" --type facts
python execution/memory_db.py search "last week" --after 2026-03-10
python execution/memory_db.py search "onboarding" --json
`

### Short-Term Memory
`ash
python execution/memory_db.py stm set "current_task" "Processing batch 3"
python execution/memory_db.py stm set "retry_count" "2" --ttl 3600    # Expires in 1hr
python execution/memory_db.py stm get "current_task"
python execution/memory_db.py stm show
python execution/memory_db.py stm clear                                # Clear expired
python execution/memory_db.py stm clear --all                         # Clear everything
`

### Long-Term Memory: Facts
`ash
python execution/memory_db.py add-fact "SerpAPI free tier: 100 searches/month" \
    --category "api_limits" --tags "serpapi,rate-limit"
python execution/memory_db.py add-fact "Client prefers bullet-point format" \
    --category "preferences" --entity "Acme Corp"
`

### Long-Term Memory: Entities
`ash
python execution/memory_db.py add-entity "Acme Corp" --type company \
    --details "Primary client, SaaS, 50 employees" --tags "client,active"
python execution/memory_db.py add-entity "Jane Doe" --type person \
    --details "CTO at Acme Corp, decision maker" --tags "contact,stakeholder"
`

### Long-Term Memory: Insights (append-only)
`ash
python execution/memory_db.py add-insight "Add 200ms delays between API calls to avoid 429s" \
    --category "api"
python execution/memory_db.py add-insight "PDF extraction is better with pymupdf than pdfplumber" \
    --category "tools"
`

### Interactions & Decisions
`ash
python execution/memory_db.py log-interaction --summary "Generated 50 leads" \
    --topics "lead-gen,google-maps" --follow-ups "Enrich emails"
    
python execution/memory_db.py log-decision --decision "Switch to direct scraping" \
    --context "Apify costs too high" --reasoning "Direct is 3x cheaper"
    
python execution/memory_db.py update-outcome 1 "Direct scraping worked, 3x savings"
`

### Context & Profile
`ash
python execution/memory_db.py context set "project.stage" "data_collection"
python execution/memory_db.py context show
python execution/memory_db.py profile set "agent.type" "lead_generation"
python execution/memory_db.py profile show
`

### Maintenance
```bash
python execution/memory_db.py status                    # Table row counts
python execution/memory_db.py rebuild-fts               # Repair search indexes
python execution/memory_db.py export --format json      # Full memory dump
```

### Embedding / Semantic Search (Optional)
Requires `pip install sentence-transformers`. Falls back to BM25 if not installed.

```bash
python execution/memory_db.py embed-sync                # Build/refresh embeddings for all facts, insights, entities
python execution/memory_db.py embed-search "rate limits" --top-k 5
python execution/memory_db.py hybrid-search "API billing" --semantic-weight 0.3 --json
```

### Memory Consolidation / Reflection
```bash
python execution/memory_db.py consolidate-stm --days 1  # Promote high-access STM to facts, discard stale
python execution/memory_db.py deduplicate-facts          # Remove exact duplicate facts
python execution/memory_db.py reflect --json             # Generate consolidation report (pending decisions, stale STM, suggestions)
```

### Evaluation & Guardrails
```bash
python execution/memory_db.py log-eval --task "scrape_leads" --status success --cost 0.10 --tokens 2000 --duration 15.0
python execution/memory_db.py check-guardrails --task "email_gen" --output-text "Hello..." --cost 0.05 --tokens 500 --json
python execution/memory_db.py eval-summary --days 7 --json
```

Guardrail checks (run automatically via `check-guardrails`):
- **output_not_empty** — Output must not be blank
- **no_sensitive_data** — Regex scan for API keys, passwords, SSNs, credit cards
- **cost_within_budget** — Daily cost tracked against `DAILY_COST_BUDGET_USD` env var (default $10)
- **token_usage_ok** — Per-task tokens against `MAX_TOKENS_PER_TASK` env var (default 100k)
- **output_length_ok** — Output must be under 1MB

## Memory Hygiene Protocol

### After EVERY substantive task:
1. **Log the interaction** — what was done, what was the outcome
2. **Store new facts** — any API limits, preferences, or constraints discovered
3. **Update entities** — any new people, companies, or tools encountered
4. **Add insights** — any lessons learned or patterns discovered
5. **Log decisions** — any choices made with reasoning

### Before EVERY new task:
1. **Search memory** for relevant context: search "<task keywords>"
2. **Check STM** for in-progress state: stm show
3. **Check context** for current project state: context show

### When errors occur (self-annealing):
1. Store the error pattern as a fact: dd-fact "X API returns 429 after 50 req/min" --category api_limits
2. Store the fix as an insight: dd-insight "Batch X API calls in groups of 40 with 2s delays" --category fixes
3. Update the directive with the learning

### Periodic maintenance:
1. Clear expired STM: stm clear
2. Consolidate STM: consolidate-stm (promotes valuable short-term entries to long-term facts)
3. Deduplicate facts: deduplicate-facts (removes exact duplicates)
4. Run reflection: reflect --json (review pending decisions, stale entries, suggestions)
5. Sync embeddings: embed-sync (if sentence-transformers installed)
6. Check decision outcomes: search for pending decisions and update outcomes
7. Export memory periodically: export --format json (save to .tmp/memory_backup.json)
8. Review evaluation summary: eval-summary --days 7

## Data Quality Rules
- Every fact should be atomic — one piece of information per row
- Use tags generously — they make search more accurate
- Keep entities deduplicated — search before creating
- Insights are append-only — never delete lessons learned
- Context reflects current state — update as things change
- STM should be cleared between tasks — don't let it grow stale

## Integration with DOE Framework

The memory system enhances the 3-layer architecture:

1. **Before executing a directive**: Search memory for relevant context and past learnings
2. **During execution**: Use STM to track task progress and state
3. **After execution**: Log interactions, store facts, add insights, log evaluation
4. **On errors**: Store error patterns and fixes (self-annealing loop)
5. **On output**: Run guardrails to validate quality and safety
6. **Periodically**: Consolidate STM, deduplicate, reflect, sync embeddings

This creates a flywheel: each task makes the agent smarter for the next one.

## Evaluation & Guardrails Protocol

### After every task that produces output:
1. **Run guardrails**: `check-guardrails --task "task_name" --output-file output.txt --cost X --tokens Y`
2. **Log evaluation**: `log-eval --task "task_name" --status success --cost X --tokens Y --duration Z`
3. **If guardrails fail**: Fix the issue, re-run, log the failure as an insight

### Daily review:
1. **Check eval summary**: `eval-summary --days 1`
2. **Review cost burn**: Are costs within budget?
3. **Check guardrail failures**: Any recurring patterns?

### Environment variables for guardrails:
- `DAILY_COST_BUDGET_USD` — Maximum daily spend (default: 10.0)
- `MAX_TOKENS_PER_TASK` — Maximum tokens per task (default: 100000)
- `EMBEDDING_MODEL` — Sentence-transformers model name (default: all-MiniLM-L6-v2)
