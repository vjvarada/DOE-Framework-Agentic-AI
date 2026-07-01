#!/usr/bin/env python3
"""
Indian Legal Compliance Checker

Generates compliance checklists, performs audits, and identifies gaps based on
company profile (type, state, employee count, turnover, industry).

Usage:
    python compliance_checker.py --mode checklist --company-type private_limited --state Maharashtra --employees 50 --output .tmp/checklist.json
    python compliance_checker.py --mode audit --company-type llp --state Karnataka --output .tmp/audit.json
    python compliance_checker.py --mode gap_analysis --company-type private_limited --state Delhi --employees 200 --current-compliance .tmp/current.json --output .tmp/gaps.json
"""

import os
import sys
import json
import argparse
from datetime import datetime, date
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ─── Compliance Database ────────────────────────────────────────────────────
# This is the core knowledge base of Indian compliance requirements.
# Organized by category, with applicability rules.

COMPLIANCE_DATABASE = {
    "company_law": {
        "roc_annual_return": {
            "name": "Annual Return Filing (MGT-7/MGT-7A)",
            "act": "Companies Act, 2013 — Section 92",
            "description": "File annual return with ROC within 60 days of AGM",
            "applicable_to": ["private_limited", "public_limited", "one_person_company", "section_8"],
            "frequency": "annual",
            "deadline_rule": "Within 60 days of AGM (AGM must be held by 30 Sep)",
            "typical_deadline": "30 Nov",
            "penalty": "₹100/day up to ₹5 Lakh; officer in default ₹50,000 to ₹5 Lakh",
            "form": "MGT-7 (Public/Large Private) or MGT-7A (Small/OPC)",
            "category": "Company Law"
        },
        "roc_financial_statements": {
            "name": "Financial Statements Filing (AOC-4/AOC-4 CFS)",
            "act": "Companies Act, 2013 — Section 137",
            "description": "File financial statements with ROC within 30 days of AGM",
            "applicable_to": ["private_limited", "public_limited", "one_person_company", "section_8"],
            "frequency": "annual",
            "deadline_rule": "Within 30 days of AGM",
            "typical_deadline": "30 Oct",
            "penalty": "₹100/day (company), ₹100/day (officer), no cap specified",
            "form": "AOC-4 or AOC-4 CFS (consolidated)",
            "category": "Company Law"
        },
        "agm": {
            "name": "Annual General Meeting",
            "act": "Companies Act, 2013 — Section 96",
            "description": "Hold AGM within 6 months from end of financial year",
            "applicable_to": ["private_limited", "public_limited", "section_8"],
            "frequency": "annual",
            "deadline_rule": "Within 6 months of FY end (by 30 Sep for Mar FY end)",
            "typical_deadline": "30 Sep",
            "penalty": "₹1 Lakh (company), ₹5,000 continuing per day",
            "form": "N/A — maintain minutes in Minutes Book",
            "category": "Company Law"
        },
        "board_meeting": {
            "name": "Board Meetings",
            "act": "Companies Act, 2013 — Section 173",
            "description": "Minimum 4 board meetings per year, gap not exceeding 120 days",
            "applicable_to": ["private_limited", "public_limited", "one_person_company", "section_8"],
            "frequency": "quarterly",
            "deadline_rule": "At least once every quarter, gap ≤120 days",
            "typical_deadline": "Every quarter",
            "penalty": "₹25,000 each director for non-attendance penalty",
            "form": "N/A — maintain Board Minutes",
            "category": "Company Law",
            "note": "OPC and small companies: minimum 2 meetings, gap ≤90 days between meetings"
        },
        "dir3_kyc": {
            "name": "Director KYC (DIR-3 KYC)",
            "act": "Companies Act, 2013 — Rule 12A",
            "description": "Annual KYC for all directors holding DIN",
            "applicable_to": ["private_limited", "public_limited", "one_person_company", "section_8", "llp"],
            "frequency": "annual",
            "deadline_rule": "By 30 September each year",
            "typical_deadline": "30 Sep",
            "penalty": "₹5,000 + DIN deactivation",
            "form": "DIR-3 KYC (web/eForm)",
            "category": "Company Law"
        },
        "statutory_audit": {
            "name": "Statutory Audit",
            "act": "Companies Act, 2013 — Section 139-147",
            "description": "Appoint auditor and get accounts audited annually",
            "applicable_to": ["private_limited", "public_limited", "one_person_company", "section_8"],
            "frequency": "annual",
            "deadline_rule": "First auditor within 30 days of incorporation; rotation every 5 years (individual) / 10 years (firm)",
            "typical_deadline": "Before AGM",
            "penalty": "₹25,000 to ₹5 Lakh",
            "form": "ADT-1 (appointment)",
            "category": "Company Law"
        },
        "commencement_of_business": {
            "name": "Commencement of Business Declaration (INC-20A)",
            "act": "Companies Act, 2013 — Section 10A",
            "description": "File declaration within 180 days of incorporation confirming capital subscription received",
            "applicable_to": ["private_limited", "public_limited"],
            "frequency": "one_time",
            "deadline_rule": "Within 180 days of incorporation",
            "typical_deadline": "Within 180 days",
            "penalty": "₹50,000 (company), ₹1,000/day (officer); potential striking off",
            "form": "INC-20A",
            "category": "Company Law"
        },
        "llp_form_8": {
            "name": "LLP Statement of Account & Solvency (Form 8)",
            "act": "LLP Act, 2008 — Section 34(2)",
            "description": "Annual statement of accounts and solvency",
            "applicable_to": ["llp"],
            "frequency": "annual",
            "deadline_rule": "Within 30 days from end of 6 months of FY (30 Oct for Mar FY)",
            "typical_deadline": "30 Oct",
            "penalty": "₹100/day per partner",
            "form": "Form 8",
            "category": "Company Law"
        },
        "llp_form_11": {
            "name": "LLP Annual Return (Form 11)",
            "act": "LLP Act, 2008 — Section 35",
            "description": "Annual return of LLP",
            "applicable_to": ["llp"],
            "frequency": "annual",
            "deadline_rule": "Within 60 days of FY end (30 May for Mar FY)",
            "typical_deadline": "30 May",
            "penalty": "₹100/day",
            "form": "Form 11",
            "category": "Company Law"
        },
        "related_party_transactions": {
            "name": "Related Party Transaction Disclosures",
            "act": "Companies Act, 2013 — Section 188, 189",
            "description": "Board/shareholder approval and disclosure for related party transactions",
            "applicable_to": ["private_limited", "public_limited", "section_8"],
            "frequency": "as_needed",
            "deadline_rule": "Prior approval before entering transaction; Form AOC-2 annually",
            "typical_deadline": "With AGM filing",
            "penalty": "Imprisonment up to 1 year and/or fine ₹25,000 to ₹5 Lakh",
            "form": "AOC-2, MBP-1 (interested director disclosure)",
            "category": "Company Law"
        },
        "csr": {
            "name": "Corporate Social Responsibility",
            "act": "Companies Act, 2013 — Section 135",
            "description": "CSR committee, spending 2% of average net profit, reporting",
            "applicable_to": ["private_limited", "public_limited"],
            "frequency": "annual",
            "deadline_rule": "Spend in each FY; carry forward unspent to Unspent CSR Account within 30 days of FY end",
            "typical_deadline": "31 Mar (spending); 30 Apr (transfer to unspent account)",
            "penalty": "2x unspent amount fine (company); 1/10th of unspent or ₹25 Lakh (officer)",
            "form": "CSR-2 (with AOC-4)",
            "category": "Company Law",
            "threshold": {"net_worth": 50000000000, "turnover": 100000000000, "net_profit": 500000000},
            "threshold_note": "Applicable if net worth ≥₹500 Cr OR turnover ≥₹1000 Cr OR net profit ≥₹5 Cr in preceding FY"
        }
    },
    "labor_law": {
        "epf_registration": {
            "name": "EPF Registration & Monthly Contribution",
            "act": "EPF & Miscellaneous Provisions Act, 1952",
            "description": "Register with EPFO and deposit monthly contributions (12% employer + 12% employee)",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8"],
            "frequency": "monthly",
            "deadline_rule": "Contribution by 15th of following month; ECR filing same deadline",
            "typical_deadline": "15th monthly",
            "penalty": "Interest @12% p.a. + damages up to 100% of arrears",
            "form": "Online ECR (Electronic Challan cum Return)",
            "category": "Labor Law",
            "employee_threshold": 20,
            "threshold_note": "Mandatory for establishments with 20+ employees (can voluntarily register with fewer)"
        },
        "esi_registration": {
            "name": "ESI Registration & Monthly Contribution",
            "act": "Employees' State Insurance Act, 1948",
            "description": "Register with ESIC and deposit contributions (3.25% employer + 0.75% employee)",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8"],
            "frequency": "monthly",
            "deadline_rule": "Contribution by 15th of following month",
            "typical_deadline": "15th monthly",
            "penalty": "Interest + damages (5%-25% of contribution)",
            "form": "Online via ESIC portal",
            "category": "Labor Law",
            "employee_threshold": 10,
            "threshold_note": "Mandatory for establishments with 10+ employees in notified areas (wage limit ₹21,000/month)"
        },
        "professional_tax": {
            "name": "Professional Tax Registration & Payment",
            "act": "State-specific Professional Tax Acts",
            "description": "Register and pay professional tax for all employees",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8"],
            "frequency": "monthly",
            "deadline_rule": "State-specific (typically by end of following month)",
            "typical_deadline": "Monthly/Annual (varies by state)",
            "penalty": "Interest + penalty (varies by state)",
            "form": "State-specific online portal",
            "category": "Labor Law",
            "state_specific": True,
            "note": "Not applicable in all states. Major states: Maharashtra, Karnataka, West Bengal, Andhra Pradesh, Telangana, Gujarat, etc."
        },
        "posh_compliance": {
            "name": "POSH (Prevention of Sexual Harassment) Compliance",
            "act": "Sexual Harassment of Women at Workplace Act, 2013",
            "description": "Constitute Internal Complaints Committee (ICC), conduct awareness programs, file annual report",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8", "startup"],
            "frequency": "annual",
            "deadline_rule": "ICC constitution: immediate on having 10+ employees; Annual report: 31 January",
            "typical_deadline": "31 Jan (annual report)",
            "penalty": "₹50,000 first offence; cancellation of registration for repeat offence",
            "form": "Annual report to District Officer",
            "category": "Labor Law",
            "employee_threshold": 10,
            "threshold_note": "Mandatory for workplaces with 10+ employees"
        },
        "gratuity": {
            "name": "Payment of Gratuity",
            "act": "Payment of Gratuity Act, 1972",
            "description": "Pay gratuity to employees with 5+ years of service upon exit",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8"],
            "frequency": "as_needed",
            "deadline_rule": "Within 30 days of it becoming payable",
            "typical_deadline": "On separation/retirement",
            "penalty": "Interest + imprisonment up to 2 years and/or fine up to ₹20,000",
            "form": "Form I (nomination), Form F (application by employee)",
            "category": "Labor Law",
            "employee_threshold": 10,
            "threshold_note": "Mandatory for establishments with 10+ employees at any point"
        },
        "maternity_benefit": {
            "name": "Maternity Benefit Compliance",
            "act": "Maternity Benefit Act, 1961 (amended 2017)",
            "description": "26 weeks paid leave (first 2 children), crèche facility (50+ employees), work-from-home option",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8"],
            "frequency": "as_needed",
            "deadline_rule": "Entitlement upon eligibility (80 days of work in 12 months preceding expected delivery)",
            "typical_deadline": "As applicable",
            "penalty": "Imprisonment 3 months to 1 year and/or fine ₹2,000 to ₹5,000",
            "form": "Various forms under the Act",
            "category": "Labor Law",
            "employee_threshold": 10,
            "threshold_note": "Applicable to all establishments with 10+ employees"
        },
        "shops_establishments": {
            "name": "Shops & Establishments Act Registration",
            "act": "State-specific Shops & Establishments Acts",
            "description": "Register establishment under state Shops Act; comply with working hours, leave, holidays",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "annual",
            "deadline_rule": "Within 30 days of starting operations; renewal as per state rules",
            "typical_deadline": "Within 30 days of commencement; annual renewal (state-specific)",
            "penalty": "Fine ₹1,000 to ₹25,000 (varies by state)",
            "form": "State-specific (usually online)",
            "category": "Labor Law",
            "state_specific": True
        },
        "labour_welfare_fund": {
            "name": "Labour Welfare Fund Contribution",
            "act": "State-specific Labour Welfare Fund Acts",
            "description": "Contribute to state labour welfare fund for all eligible employees",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8"],
            "frequency": "half_yearly",
            "deadline_rule": "State-specific (typically June and December)",
            "typical_deadline": "Jun/Dec or Jan/Jul (varies)",
            "penalty": "Varies by state",
            "form": "State-specific",
            "category": "Labor Law",
            "state_specific": True,
            "note": "Not applicable in all states. Check state-specific rules."
        },
        "minimum_wages": {
            "name": "Minimum Wages Compliance",
            "act": "Code on Wages, 2019 / Minimum Wages Act, 1948",
            "description": "Pay at least minimum wages as notified by Central/State government",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "ongoing",
            "deadline_rule": "Continuous — wages must meet or exceed notified minimums",
            "typical_deadline": "Each pay cycle",
            "penalty": "Fine up to ₹50,000; repeat offence: imprisonment up to 3 months and/or fine ₹1 Lakh",
            "form": "Maintain registers and wage slips",
            "category": "Labor Law"
        },
        "contract_labour": {
            "name": "Contract Labour Compliance",
            "act": "Contract Labour (Regulation & Abolition) Act, 1970",
            "description": "Principal employer registration; contractor license; maintain registers",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8"],
            "frequency": "annual",
            "deadline_rule": "Registration before engaging contract labour; license renewal annually",
            "typical_deadline": "Before engagement; annual renewal",
            "penalty": "Imprisonment up to 3 months and/or fine up to ₹1,000",
            "form": "Form I (registration), Form IV (license)",
            "category": "Labor Law",
            "employee_threshold": 20,
            "threshold_note": "Applicable when 20+ contract workers employed on any day in preceding 12 months"
        }
    },
    "tax_compliance": {
        "gst_registration": {
            "name": "GST Registration",
            "act": "CGST Act, 2017 — Section 22",
            "description": "Mandatory GST registration if turnover exceeds threshold",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "one_time",
            "deadline_rule": "Within 30 days of becoming liable",
            "typical_deadline": "Within 30 days of crossing threshold",
            "penalty": "₹10,000 or 10% of tax due, whichever is higher",
            "form": "GST REG-01",
            "category": "Tax",
            "note": "Threshold: ₹40L goods / ₹20L services (₹20L/₹10L for special category states)"
        },
        "gst_returns": {
            "name": "GST Return Filing (GSTR-1, GSTR-3B)",
            "act": "CGST Act, 2017 — Section 39",
            "description": "Monthly/quarterly filing of GST returns",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "monthly",
            "deadline_rule": "GSTR-1: 11th of following month; GSTR-3B: 20th of following month",
            "typical_deadline": "11th and 20th monthly",
            "penalty": "₹50/day (CGST+SGST) up to ₹10,000 per return + 18% interest on tax",
            "form": "GSTR-1, GSTR-3B",
            "category": "Tax"
        },
        "gst_annual_return": {
            "name": "GST Annual Return (GSTR-9)",
            "act": "CGST Act, 2017 — Section 44",
            "description": "Annual return consolidating all monthly returns",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "annual",
            "deadline_rule": "31 December of following financial year",
            "typical_deadline": "31 Dec",
            "penalty": "₹200/day (CGST+SGST) up to 0.25% of turnover",
            "form": "GSTR-9 / GSTR-9C (if turnover > ₹5 Cr)",
            "category": "Tax"
        },
        "tds_deposit": {
            "name": "TDS Deposit",
            "act": "Income Tax Act, 1961 — Section 192-206",
            "description": "Deduct and deposit TDS on salary, professional fees, rent, etc.",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8", "startup"],
            "frequency": "monthly",
            "deadline_rule": "7th of following month (March: 30 April)",
            "typical_deadline": "7th monthly",
            "penalty": "Interest @1.5% per month + penalty equal to TDS amount",
            "form": "Challan 281",
            "category": "Tax"
        },
        "tds_returns": {
            "name": "TDS Return Filing",
            "act": "Income Tax Act, 1961 — Section 200(3)",
            "description": "Quarterly TDS returns — 24Q (salary), 26Q (non-salary), 27Q (NRI payments)",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8", "startup"],
            "frequency": "quarterly",
            "deadline_rule": "31st of month following quarter (Q4: 31 May)",
            "typical_deadline": "31 Jul, 31 Oct, 31 Jan, 31 May",
            "penalty": "₹200/day until filed; minimum ₹10,000 to ₹1 Lakh late fee",
            "form": "24Q, 26Q, 27Q, 27EQ",
            "category": "Tax"
        },
        "income_tax_return": {
            "name": "Income Tax Return Filing",
            "act": "Income Tax Act, 1961 — Section 139",
            "description": "Annual income tax return filing for the company",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "annual",
            "deadline_rule": "31 Oct (if audit required) / 31 Jul (otherwise)",
            "typical_deadline": "31 Oct (most companies)",
            "penalty": "₹5,000 (if filed by 31 Dec) / ₹10,000 (after); Sec 234A/B/C interest",
            "form": "ITR-6 (companies), ITR-5 (LLP/partnership), ITR-3 (sole prop)",
            "category": "Tax"
        },
        "advance_tax": {
            "name": "Advance Tax Payment",
            "act": "Income Tax Act, 1961 — Section 208-211",
            "description": "Quarterly advance tax installments if tax liability > ₹10,000",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "section_8", "startup"],
            "frequency": "quarterly",
            "deadline_rule": "15 Jun (15%), 15 Sep (45%), 15 Dec (75%), 15 Mar (100%)",
            "typical_deadline": "15 Jun, 15 Sep, 15 Dec, 15 Mar",
            "penalty": "Interest under Sec 234B (shortfall) and Sec 234C (deferment)",
            "form": "Challan 280",
            "category": "Tax"
        },
        "tax_audit": {
            "name": "Tax Audit (Section 44AB)",
            "act": "Income Tax Act, 1961 — Section 44AB",
            "description": "Get accounts audited if turnover exceeds threshold",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "annual",
            "deadline_rule": "30 September of assessment year",
            "typical_deadline": "30 Sep",
            "penalty": "0.5% of turnover or ₹1.5 Lakh, whichever is lower",
            "form": "Form 3CA-3CD / 3CB-3CD",
            "category": "Tax",
            "note": "Threshold: ₹1 Cr turnover (business) / ₹50 Lakh (profession); ₹10 Cr if 95%+ digital transactions"
        },
        "e_invoicing": {
            "name": "E-Invoicing under GST",
            "act": "CGST Rules — Notification 13/2020",
            "description": "Generate e-invoices through IRP for B2B transactions",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "ongoing",
            "deadline_rule": "Real-time generation for each B2B invoice",
            "typical_deadline": "Each invoice",
            "penalty": "₹25,000 per invoice (100% of tax amount)",
            "form": "Via IRP portal / GST-enabled software",
            "category": "Tax",
            "note": "Mandatory if aggregate turnover > ₹5 Cr in any FY from 2017-18"
        }
    },
    "ip_compliance": {
        "trademark_registration": {
            "name": "Trademark Registration & Renewal",
            "act": "Trade Marks Act, 1999",
            "description": "Register and renew trademarks to protect brand identity",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "every_10_years",
            "deadline_rule": "Renewal every 10 years from registration; apply 6 months before expiry",
            "typical_deadline": "6 months before 10-year expiry",
            "penalty": "Loss of trademark protection if not renewed",
            "form": "TM-A (application), TM-R (renewal)",
            "category": "Intellectual Property"
        },
        "patent_renewal": {
            "name": "Patent Renewal",
            "act": "Patents Act, 1970 — Section 53",
            "description": "Annual renewal fees from 3rd year of patent grant",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "annual",
            "deadline_rule": "Before expiry of each year (from 3rd year); can pay within 6 months after with surcharge",
            "typical_deadline": "Annual from 3rd year",
            "penalty": "Patent ceases to have effect if renewal not paid",
            "form": "Form 4 (renewal request)",
            "category": "Intellectual Property"
        },
        "data_protection": {
            "name": "Data Protection Compliance (DPDP Act)",
            "act": "Digital Personal Data Protection Act, 2023",
            "description": "Consent management, data processing agreements, breach notification, grievance redressal",
            "applicable_to": ["private_limited", "public_limited", "llp", "one_person_company", "partnership", "sole_proprietorship", "section_8", "startup"],
            "frequency": "ongoing",
            "deadline_rule": "Continuous compliance; breach notification to DPB 'without delay'",
            "typical_deadline": "Ongoing",
            "penalty": "Up to ₹250 Cr per violation",
            "form": "As prescribed by Data Protection Board rules (awaited)",
            "category": "Intellectual Property / Data Privacy",
            "note": "Rules still being finalized. Prepare by establishing consent mechanisms, privacy policy, DPO appointment (if significant data fiduciary)."
        }
    }
}

# State-specific professional tax and shops & establishments info
STATE_SPECIFIC = {
    "Maharashtra": {
        "professional_tax": True,
        "pt_rates": "Max ₹2,500/year for salary > ₹10,000/month",
        "pt_deadline": "Monthly by last date of month",
        "shops_act": "Maharashtra Shops and Establishments (Regulation of Employment and Conditions of Service) Act, 2017",
        "shops_renewal": "No renewal needed (lifetime registration)",
        "lwf": True,
        "lwf_rate": "₹12 employee + ₹36 employer (half-yearly)"
    },
    "Karnataka": {
        "professional_tax": True,
        "pt_rates": "Max ₹2,500/year for salary > ₹15,000/month",
        "pt_deadline": "Monthly by 20th of following month",
        "shops_act": "Karnataka Shops and Commercial Establishments Act, 1961",
        "shops_renewal": "Annual renewal",
        "lwf": True,
        "lwf_rate": "₹10 employee + ₹20 employer (annual)"
    },
    "Delhi": {
        "professional_tax": False,
        "shops_act": "Delhi Shops and Establishments Act, 1954",
        "shops_renewal": "Triennial renewal (every 3 years)",
        "lwf": False
    },
    "Tamil Nadu": {
        "professional_tax": True,
        "pt_rates": "Max ₹2,500/year for salary > ₹21,000/month (half-yearly payment)",
        "pt_deadline": "Half-yearly (Apr-Sep: by 30 Sep; Oct-Mar: by 31 Mar)",
        "shops_act": "Tamil Nadu Shops and Establishments Act, 1947",
        "shops_renewal": "Annual renewal",
        "lwf": True,
        "lwf_rate": "₹5 employee + ₹10 employer (annual)"
    },
    "Telangana": {
        "professional_tax": True,
        "pt_rates": "Max ₹2,500/year for salary > ₹20,000/month",
        "pt_deadline": "Monthly by 10th of following month",
        "shops_act": "Telangana Shops and Establishments Act, 1988",
        "shops_renewal": "Once every 5 years",
        "lwf": False
    },
    "Gujarat": {
        "professional_tax": True,
        "pt_rates": "Max ₹2,500/year for salary > ₹12,000/month",
        "pt_deadline": "Monthly by 15th of following month",
        "shops_act": "Gujarat Shops and Establishments Act, 2019",
        "shops_renewal": "Lifetime registration",
        "lwf": False
    },
    "West Bengal": {
        "professional_tax": True,
        "pt_rates": "Max ₹2,500/year based on salary slabs",
        "pt_deadline": "Monthly",
        "shops_act": "West Bengal Shops and Establishments Act, 1963",
        "shops_renewal": "Annual renewal",
        "lwf": True,
        "lwf_rate": "₹3 employee + ₹6 employer (half-yearly)"
    },
    "Uttar Pradesh": {
        "professional_tax": False,
        "shops_act": "UP Shops and Commercial Establishments Act, 1962",
        "shops_renewal": "Annual renewal",
        "lwf": False
    },
    "Rajasthan": {
        "professional_tax": False,
        "shops_act": "Rajasthan Shops and Commercial Establishments Act, 1958",
        "shops_renewal": "Annual renewal",
        "lwf": True,
        "lwf_rate": "₹10 employee + ₹20 employer (half-yearly)"
    },
    "Andhra Pradesh": {
        "professional_tax": True,
        "pt_rates": "Max ₹2,500/year for salary > ₹20,000/month",
        "pt_deadline": "Monthly by 10th of following month",
        "shops_act": "AP Shops and Establishments Act, 1988",
        "shops_renewal": "Once every 5 years",
        "lwf": False
    },
    "Kerala": {
        "professional_tax": True,
        "pt_rates": "Max ₹2,500/year for salary > ₹12,000/month",
        "pt_deadline": "Half-yearly",
        "shops_act": "Kerala Shops and Commercial Establishments Act, 1960",
        "shops_renewal": "Annual renewal",
        "lwf": True,
        "lwf_rate": "₹2 per head per half year"
    },
    "Madhya Pradesh": {
        "professional_tax": True,
        "pt_rates": "Max ₹2,500/year for salary > ₹18,750/month",
        "pt_deadline": "Monthly",
        "shops_act": "MP Shops and Establishments Act, 1958",
        "shops_renewal": "Triennial renewal",
        "lwf": True,
        "lwf_rate": "Employer contribution only"
    }
}


def get_applicable_compliances(company_type: str, state: str = None,
                               employees: int = None, turnover: float = None,
                               industry: str = None) -> list:
    """
    Determine which compliance requirements apply to a given company profile.
    Returns a sorted list of compliance items with applicability details.
    """
    applicable = []
    
    for category_key, category_items in COMPLIANCE_DATABASE.items():
        for item_key, item in category_items.items():
            # Check if company type is applicable
            if company_type not in item.get("applicable_to", []):
                continue
            
            # Check employee threshold
            threshold = item.get("employee_threshold")
            if threshold and employees is not None and employees < threshold:
                item_copy = item.copy()
                item_copy["status"] = "not_yet_applicable"
                item_copy["reason"] = f"Requires {threshold}+ employees (currently {employees})"
                item_copy["id"] = item_key
                applicable.append(item_copy)
                continue
            
            item_copy = item.copy()
            item_copy["status"] = "applicable"
            item_copy["id"] = item_key
            applicable.append(item_copy)
    
    # Add state-specific information
    if state and state in STATE_SPECIFIC:
        state_info = STATE_SPECIFIC[state]
        
        # Update professional tax entry
        for item in applicable:
            if item["id"] == "professional_tax":
                if not state_info.get("professional_tax"):
                    item["status"] = "not_applicable"
                    item["reason"] = f"Professional Tax not applicable in {state}"
                else:
                    item["state_details"] = {
                        "rates": state_info.get("pt_rates", "Check state notification"),
                        "deadline": state_info.get("pt_deadline", "Check state rules")
                    }
            
            if item["id"] == "shops_establishments":
                item["state_details"] = {
                    "act": state_info.get("shops_act", "State Shops & Establishments Act"),
                    "renewal": state_info.get("shops_renewal", "Check state rules")
                }
            
            if item["id"] == "labour_welfare_fund":
                if not state_info.get("lwf"):
                    item["status"] = "not_applicable"
                    item["reason"] = f"Labour Welfare Fund not applicable in {state}"
                else:
                    item["state_details"] = {
                        "rate": state_info.get("lwf_rate", "Check state notification")
                    }
    
    # Sort by category and status
    priority_order = {"applicable": 0, "not_yet_applicable": 1, "not_applicable": 2}
    applicable.sort(key=lambda x: (priority_order.get(x.get("status", "applicable"), 3), x.get("category", "")))
    
    return applicable


def generate_checklist(company_type: str, state: str = None,
                      employees: int = None, turnover: float = None,
                      industry: str = None) -> dict:
    """Generate a comprehensive compliance checklist."""
    items = get_applicable_compliances(company_type, state, employees, turnover, industry)
    
    applicable_items = [i for i in items if i["status"] == "applicable"]
    pending_items = [i for i in items if i["status"] == "not_yet_applicable"]
    na_items = [i for i in items if i["status"] == "not_applicable"]
    
    checklist = {
        "company_profile": {
            "company_type": company_type,
            "state": state,
            "employees": employees,
            "turnover": turnover,
            "industry": industry
        },
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_items": len(items),
            "applicable": len(applicable_items),
            "not_yet_applicable": len(pending_items),
            "not_applicable": len(na_items)
        },
        "applicable_compliances": applicable_items,
        "upcoming_thresholds": pending_items,
        "not_applicable": na_items,
        "state_specific_info": STATE_SPECIFIC.get(state, {"note": f"State-specific details not yet mapped for {state}. Please verify locally."}),
        "disclaimer": "This checklist is for informational purposes only and does not constitute legal advice. "
                      "Laws and regulations change frequently. Please consult a qualified legal professional."
    }
    
    return checklist


def perform_audit(company_type: str, state: str = None,
                 employees: int = None, turnover: float = None) -> dict:
    """Perform a compliance audit - list all requirements with risk levels."""
    items = get_applicable_compliances(company_type, state, employees, turnover)
    
    audit_results = []
    for item in items:
        if item["status"] != "applicable":
            continue
        
        risk_level = "HIGH" if "imprisonment" in item.get("penalty", "").lower() or \
                              "cancellation" in item.get("penalty", "").lower() else \
                     "MEDIUM" if "₹" in item.get("penalty", "") else "LOW"
        
        audit_results.append({
            "id": item["id"],
            "name": item["name"],
            "act": item["act"],
            "category": item["category"],
            "frequency": item["frequency"],
            "deadline": item["typical_deadline"],
            "risk_level": risk_level,
            "penalty_summary": item.get("penalty", "N/A"),
            "form": item.get("form", "N/A"),
            "status": "NEEDS_REVIEW"
        })
    
    return {
        "audit_type": "compliance_audit",
        "generated_at": datetime.now().isoformat(),
        "company_type": company_type,
        "state": state,
        "total_requirements": len(audit_results),
        "high_risk": len([r for r in audit_results if r["risk_level"] == "HIGH"]),
        "medium_risk": len([r for r in audit_results if r["risk_level"] == "MEDIUM"]),
        "low_risk": len([r for r in audit_results if r["risk_level"] == "LOW"]),
        "requirements": audit_results,
        "disclaimer": "This audit is for informational purposes only. Engage a qualified CA/CS for a formal compliance audit."
    }


def gap_analysis(company_type: str, state: str, employees: int,
                current_compliance_file: str = None, turnover: float = None) -> dict:
    """
    Compare required compliances against current status to identify gaps.
    """
    required = get_applicable_compliances(company_type, state, employees, turnover)
    applicable_required = [i for i in required if i["status"] == "applicable"]
    
    current_status = {}
    if current_compliance_file and Path(current_compliance_file).exists():
        with open(current_compliance_file, "r", encoding="utf-8") as f:
            current_data = json.load(f)
            # Expected format: {"completed": ["item_id1", "item_id2"], "in_progress": [...]}
            for item_id in current_data.get("completed", []):
                current_status[item_id] = "completed"
            for item_id in current_data.get("in_progress", []):
                current_status[item_id] = "in_progress"
    
    gaps = []
    compliant = []
    in_progress = []
    
    for item in applicable_required:
        item_id = item["id"]
        status = current_status.get(item_id, "missing")
        
        if status == "completed":
            compliant.append({
                "id": item_id,
                "name": item["name"],
                "category": item["category"],
                "status": "COMPLIANT"
            })
        elif status == "in_progress":
            in_progress.append({
                "id": item_id,
                "name": item["name"],
                "category": item["category"],
                "deadline": item.get("typical_deadline"),
                "status": "IN_PROGRESS"
            })
        else:
            risk = "HIGH" if "imprisonment" in item.get("penalty", "").lower() else "MEDIUM"
            gaps.append({
                "id": item_id,
                "name": item["name"],
                "act": item["act"],
                "category": item["category"],
                "deadline": item.get("typical_deadline"),
                "penalty": item.get("penalty"),
                "risk_level": risk,
                "status": "GAP",
                "remediation": f"Initiate compliance for {item['name']} immediately"
            })
    
    return {
        "analysis_type": "gap_analysis",
        "generated_at": datetime.now().isoformat(),
        "company_type": company_type,
        "state": state,
        "employees": employees,
        "summary": {
            "total_required": len(applicable_required),
            "compliant": len(compliant),
            "in_progress": len(in_progress),
            "gaps": len(gaps),
            "compliance_score": f"{(len(compliant) / max(len(applicable_required), 1)) * 100:.1f}%"
        },
        "gaps": sorted(gaps, key=lambda x: 0 if x["risk_level"] == "HIGH" else 1),
        "in_progress": in_progress,
        "compliant": compliant,
        "disclaimer": "This gap analysis is for informational purposes only. Engage a qualified CS/CA for formal assessment."
    }


def main():
    parser = argparse.ArgumentParser(description="Indian Legal Compliance Checker")
    parser.add_argument("--mode", required=True, choices=["checklist", "audit", "gap_analysis"],
                       help="Operation mode")
    parser.add_argument("--company-type", required=True,
                       choices=["private_limited", "public_limited", "llp", "one_person_company",
                               "partnership", "sole_proprietorship", "section_8", "startup"],
                       help="Type of company")
    parser.add_argument("--state", help="Indian state of registration")
    parser.add_argument("--employees", type=int, help="Number of employees")
    parser.add_argument("--turnover", type=float, help="Annual turnover in INR")
    parser.add_argument("--industry", help="Industry sector")
    parser.add_argument("--current-compliance", help="Path to current compliance status JSON (for gap analysis)")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--copilot", action="store_true",
                       help="Copilot mode — output prompt for Copilot to analyze results")
    
    args = parser.parse_args()
    
    # Ensure output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"COMPLIANCE CHECKER — Mode: {args.mode}")
    print(f"{'='*60}")
    print(f"  Company Type: {args.company_type}")
    if args.state:
        print(f"  State: {args.state}")
    if args.employees:
        print(f"  Employees: {args.employees}")
    if args.turnover:
        print(f"  Turnover: ₹{args.turnover:,.0f}")
    
    if args.mode == "checklist":
        result = generate_checklist(
            args.company_type, args.state, args.employees, args.turnover, args.industry
        )
    elif args.mode == "audit":
        result = perform_audit(
            args.company_type, args.state, args.employees, args.turnover
        )
    elif args.mode == "gap_analysis":
        result = gap_analysis(
            args.company_type, args.state, args.employees,
            args.current_compliance, args.turnover
        )
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to {output_path}")
    
    if args.mode == "checklist":
        s = result["summary"]
        print(f"  Applicable: {s['applicable']} | Upcoming: {s['not_yet_applicable']} | N/A: {s['not_applicable']}")
    elif args.mode == "audit":
        print(f"  Total: {result['total_requirements']} | High Risk: {result['high_risk']} | Medium: {result['medium_risk']}")
    elif args.mode == "gap_analysis":
        s = result["summary"]
        print(f"  Score: {s['compliance_score']} | Gaps: {s['gaps']} | Compliant: {s['compliant']}")
    
    if args.copilot:
        print(f"\n{'='*60}")
        print("COPILOT MODE — Analyze these results:")
        print(f"{'='*60}")
        print(f"\nReview the compliance {args.mode} in {output_path}.")
        print("Provide a clear summary covering:")
        print("1. Critical/high-risk items requiring immediate attention")
        print("2. Upcoming deadlines in the next 30 days")
        print("3. Practical recommendations for each gap")
        print("4. Cost estimates for professional assistance where applicable")
    
    return result


if __name__ == "__main__":
    main()
