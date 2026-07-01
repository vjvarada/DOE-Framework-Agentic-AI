---
name: bill-extraction
description: >
  Extract structured data from PDF bills and receipts.
  Handles multiple vendor formats (DeepSeek, OpenAI, AWS, etc.).
  Use when the user provides PDF bills/receipts and needs data extraction.
when_to_use: User provides PDF bills or receipts for processing
authority: read
cost_tier: 1
version: 0.1.0
---

# Bill Extraction

Extracts vendor name, date, amounts, tax, line items, and payment info from PDF bills.

## Scripts

| Script | Purpose |
|--------|---------|
| scripts/extract_bills.py | Extract data from a folder of PDF bills into JSON |

## Usage

`ash
python .github/skills/bill-extraction/scripts/extract_bills.py --input "bills/" --output "outputs/campaign/step_1_bills.json"
`

## Outputs

Writes to outputs/{campaign-slug}/step_1_bills.json with structured bill data.
