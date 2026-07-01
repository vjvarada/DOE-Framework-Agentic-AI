---
name: bill-summarization
description: >
  Aggregates extracted bill data into summary tables grouped by vendor or month.
  Computes totals, tax breakdowns, and generates email-ready markdown.
  Use after bill extraction to prepare reimbursement summaries.
when_to_use: User wants to summarize multiple bills for reimbursement
authority: read
cost_tier: 1
version: 0.1.0
---

# Bill Summarization

Aggregates bills, computes totals, and generates summary tables.

## Scripts

| Script | Purpose |
|--------|---------|
| scripts/summarize_bills.py | Group bills, compute totals, generate markdown |

## Usage

`ash
python .github/skills/bill-summarization/scripts/summarize_bills.py --input "step_1_bills.json" --output "outputs/campaign/step_2"
python .github/skills/bill-summarization/scripts/summarize_bills.py --input "step_1_bills.json" --output "step_2" --group-by month
`

## Outputs

Writes step_2_summary.json and step_2_summary.md to the output path.
