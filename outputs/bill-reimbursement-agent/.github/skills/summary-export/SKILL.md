---
name: summary-export
description: >
  Generates professional PDF reimbursement reports and email drafts
  from bill summary data. Use after summarization to create
  submission-ready outputs for accounts teams.
when_to_use: User wants to export a reimbursement report as PDF or email
authority: write
cost_tier: 1
version: 0.1.0
---

# Summary Export

Creates PDF reports and email drafts from bill summaries.

## Scripts

| Script | Purpose |
|--------|---------|
| scripts/generate_bill_summary.py | Generate PDF report + email draft |

## Usage

`ash
python .github/skills/summary-export/scripts/generate_bill_summary.py --input "step_2_summary.json" --output "outputs/campaign/"
`

## Outputs

Writes eimbursement_report.pdf and eimbursement_email.txt.
