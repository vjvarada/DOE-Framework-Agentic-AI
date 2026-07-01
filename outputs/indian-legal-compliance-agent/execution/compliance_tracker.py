#!/usr/bin/env python3
"""
Indian Legal Compliance Tracker

Manages compliance deadlines in Google Sheets. Initializes a tracker from
a compliance checklist, tracks completion status, and reports upcoming/overdue items.

Usage:
    python compliance_tracker.py --mode init --company "Acme Pvt Ltd" --checklist .tmp/checklist.json --sheet-id SHEET_ID --output .tmp/init.json
    python compliance_tracker.py --mode upcoming --sheet-id SHEET_ID --days 30 --output .tmp/upcoming.json
    python compliance_tracker.py --mode overdue --sheet-id SHEET_ID --output .tmp/overdue.json
    python compliance_tracker.py --mode update --sheet-id SHEET_ID --item-id "epf_registration" --status completed --date "2024-01-15" --output .tmp/update.json
"""

import os
import sys
import json
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try to import Google Sheets libraries
try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# ─── Compliance Calendar ────────────────────────────────────────────────────
# Standard deadlines for a March 31 financial year

COMPLIANCE_CALENDAR = {
    # Monthly deadlines
    "monthly": [
        {"day": 7, "item": "TDS Deposit", "category": "Tax", "form": "Challan 281"},
        {"day": 11, "item": "GSTR-1 Filing", "category": "Tax", "form": "GSTR-1"},
        {"day": 15, "item": "EPF Contribution & ECR", "category": "Labor", "form": "ECR"},
        {"day": 15, "item": "ESI Contribution", "category": "Labor", "form": "ESIC Challan"},
        {"day": 20, "item": "GSTR-3B Filing", "category": "Tax", "form": "GSTR-3B"},
    ],
    # Quarterly deadlines
    "quarterly": {
        "Q1": [
            {"date": "07-31", "item": "TDS Return (Q1: Apr-Jun)", "category": "Tax", "form": "24Q/26Q/27Q"},
        ],
        "Q2": [
            {"date": "10-31", "item": "TDS Return (Q2: Jul-Sep)", "category": "Tax", "form": "24Q/26Q/27Q"},
        ],
        "Q3": [
            {"date": "01-31", "item": "TDS Return (Q3: Oct-Dec)", "category": "Tax", "form": "24Q/26Q/27Q"},
            {"date": "01-31", "item": "POSH Annual Report", "category": "Labor", "form": "Annual Report to District Officer"},
        ],
        "Q4": [
            {"date": "05-31", "item": "TDS Return (Q4: Jan-Mar)", "category": "Tax", "form": "24Q/26Q/27Q"},
        ]
    },
    # Annual deadlines (date format: MM-DD)
    "annual": [
        {"date": "05-30", "item": "LLP Form 11 (Annual Return)", "category": "Company Law", "form": "Form 11", "entity": ["llp"]},
        {"date": "06-15", "item": "Advance Tax - 1st Installment (15%)", "category": "Tax", "form": "Challan 280"},
        {"date": "09-15", "item": "Advance Tax - 2nd Installment (45%)", "category": "Tax", "form": "Challan 280"},
        {"date": "09-30", "item": "AGM (Annual General Meeting)", "category": "Company Law", "form": "Minutes Book"},
        {"date": "09-30", "item": "DIR-3 KYC (Director KYC)", "category": "Company Law", "form": "DIR-3 KYC"},
        {"date": "09-30", "item": "Tax Audit Report (Sec 44AB)", "category": "Tax", "form": "Form 3CA-3CD"},
        {"date": "10-30", "item": "LLP Form 8 (Statement of Account)", "category": "Company Law", "form": "Form 8", "entity": ["llp"]},
        {"date": "10-30", "item": "AOC-4 Financial Statements", "category": "Company Law", "form": "AOC-4"},
        {"date": "10-31", "item": "Income Tax Return Filing", "category": "Tax", "form": "ITR-6"},
        {"date": "11-29", "item": "Annual Return MGT-7/MGT-7A", "category": "Company Law", "form": "MGT-7/MGT-7A"},
        {"date": "12-15", "item": "Advance Tax - 3rd Installment (75%)", "category": "Tax", "form": "Challan 280"},
        {"date": "12-31", "item": "GST Annual Return (GSTR-9)", "category": "Tax", "form": "GSTR-9"},
        {"date": "03-15", "item": "Advance Tax - 4th Installment (100%)", "category": "Tax", "form": "Challan 280"},
    ]
}


def get_sheets_service():
    """Authenticate and return Google Sheets service."""
    if not SHEETS_AVAILABLE:
        print("ERROR: Google API libraries not installed.")
        print("Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        sys.exit(1)
    
    creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")
    if not creds_file:
        print("ERROR: Set GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_SHEETS_CREDENTIALS_FILE in .env")
        sys.exit(1)
    
    if not Path(creds_file).exists():
        print(f"ERROR: Credentials file not found: {creds_file}")
        sys.exit(1)
    
    creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service


def init_tracker(company: str, checklist_file: str, sheet_id: str = None) -> dict:
    """
    Initialize a compliance tracker from a checklist JSON.
    Creates rows in Google Sheets or returns data for manual creation.
    """
    # Load checklist
    with open(checklist_file, "r", encoding="utf-8") as f:
        checklist = json.load(f)
    
    applicable = checklist.get("applicable_compliances", [])
    
    # Build tracker rows
    headers = [
        "ID", "Compliance Item", "Category", "Act/Law", "Frequency",
        "Deadline", "Form/Filing", "Status", "Last Completed",
        "Next Due Date", "Assigned To", "Notes", "Risk Level"
    ]
    
    rows = [headers]
    today = date.today()
    
    for item in applicable:
        risk = "HIGH" if "imprisonment" in item.get("penalty", "").lower() else \
               "MEDIUM" if "₹" in item.get("penalty", "") else "LOW"
        
        rows.append([
            item.get("id", ""),
            item.get("name", ""),
            item.get("category", ""),
            item.get("act", ""),
            item.get("frequency", ""),
            item.get("typical_deadline", ""),
            item.get("form", ""),
            "NOT STARTED",
            "",
            calculate_next_due(item.get("frequency", ""), item.get("typical_deadline", ""), today),
            "",
            item.get("note", ""),
            risk
        ])
    
    # Add calendar items
    rows.append(["", "", "", "", "", "", "", "", "", "", "", "", ""])
    rows.append(["--- COMPLIANCE CALENDAR ---", "", "", "", "", "", "", "", "", "", "", "", ""])
    
    for annual in COMPLIANCE_CALENDAR["annual"]:
        month, day_num = annual["date"].split("-")
        next_due = f"{today.year}-{month}-{day_num}"
        if date.fromisoformat(next_due) < today:
            next_due = f"{today.year + 1}-{month}-{day_num}"
        
        rows.append([
            f"cal_{annual['item'].lower().replace(' ', '_')[:30]}",
            annual["item"],
            annual["category"],
            "",
            "annual",
            annual["date"],
            annual.get("form", ""),
            "PENDING",
            "",
            next_due,
            "",
            "",
            "MEDIUM"
        ])
    
    result = {
        "company": company,
        "created_at": datetime.now().isoformat(),
        "total_items": len(rows) - 1,
        "headers": headers,
        "data": rows
    }
    
    # Write to Google Sheet if sheet_id provided
    if sheet_id:
        try:
            service = get_sheets_service()
            sheet = service.spreadsheets()
            
            # Clear existing data and write new
            sheet.values().clear(
                spreadsheetId=sheet_id,
                range="Compliance Tracker!A:M"
            ).execute()
            
            sheet.values().update(
                spreadsheetId=sheet_id,
                range="Compliance Tracker!A1",
                valueInputOption="USER_ENTERED",
                body={"values": rows}
            ).execute()
            
            result["sheet_id"] = sheet_id
            result["sheet_updated"] = True
            print(f"  ✓ Google Sheet updated: {sheet_id}")
        except Exception as e:
            result["sheet_error"] = str(e)
            print(f"  ⚠ Could not update Google Sheet: {e}")
            print(f"  Data saved to output file for manual import")
    else:
        result["note"] = "No sheet_id provided. Data saved locally — import to Google Sheets manually or provide --sheet-id"
    
    return result


def calculate_next_due(frequency: str, deadline: str, from_date: date) -> str:
    """Calculate the next due date based on frequency and deadline pattern."""
    if not deadline:
        return ""
    
    if frequency == "monthly":
        # Extract day number
        try:
            day_match = __import__("re").search(r'(\d+)', deadline)
            if day_match:
                day_num = int(day_match.group(1))
                next_month = from_date.month + 1
                year = from_date.year
                if next_month > 12:
                    next_month = 1
                    year += 1
                return f"{year}-{next_month:02d}-{min(day_num, 28):02d}"
        except:
            pass
    
    elif frequency == "quarterly":
        # Next quarter end
        quarter = (from_date.month - 1) // 3 + 1
        next_q_month = quarter * 3 + 1
        year = from_date.year
        if next_q_month > 12:
            next_q_month = 1
            year += 1
        return f"{year}-{next_q_month:02d}-01"
    
    elif frequency == "annual":
        # Try to parse the deadline
        parts = deadline.split()
        month_map = {
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
            "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
            "January": 1, "February": 2, "March": 3, "April": 4,
            "June": 6, "July": 7, "August": 8, "September": 9,
            "October": 10, "November": 11, "December": 12
        }
        
        for part in parts:
            day_clean = part.strip(",").strip()
            if day_clean in month_map:
                month = month_map[day_clean]
                # Find the day number
                for p2 in parts:
                    try:
                        day_num = int(p2.strip(",").strip())
                        if 1 <= day_num <= 31:
                            next_date = date(from_date.year, month, min(day_num, 28))
                            if next_date < from_date:
                                next_date = date(from_date.year + 1, month, min(day_num, 28))
                            return next_date.isoformat()
                    except ValueError:
                        continue
    
    return deadline


def get_upcoming(sheet_id: str, days: int = 30) -> dict:
    """Get compliance items due in the next N days."""
    service = get_sheets_service()
    sheet = service.spreadsheets()
    
    result = sheet.values().get(
        spreadsheetId=sheet_id,
        range="Compliance Tracker!A:M"
    ).execute()
    
    rows = result.get("values", [])
    if not rows:
        return {"error": "No data found in sheet"}
    
    headers = rows[0]
    today = date.today()
    cutoff = today + timedelta(days=days)
    
    upcoming = []
    for row in rows[1:]:
        if len(row) < 10:
            continue
        
        next_due = row[9] if len(row) > 9 else ""
        status = row[7] if len(row) > 7 else ""
        
        if status in ("COMPLETED", "N/A"):
            continue
        
        try:
            due_date = date.fromisoformat(next_due)
            if today <= due_date <= cutoff:
                upcoming.append({
                    "id": row[0],
                    "item": row[1],
                    "category": row[2],
                    "deadline": next_due,
                    "days_remaining": (due_date - today).days,
                    "form": row[6] if len(row) > 6 else "",
                    "status": status,
                    "risk": row[12] if len(row) > 12 else ""
                })
        except (ValueError, IndexError):
            continue
    
    upcoming.sort(key=lambda x: x["days_remaining"])
    
    return {
        "query": f"Items due within {days} days",
        "generated_at": datetime.now().isoformat(),
        "today": today.isoformat(),
        "cutoff": cutoff.isoformat(),
        "count": len(upcoming),
        "items": upcoming
    }


def get_overdue(sheet_id: str) -> dict:
    """Get overdue compliance items."""
    service = get_sheets_service()
    sheet = service.spreadsheets()
    
    result = sheet.values().get(
        spreadsheetId=sheet_id,
        range="Compliance Tracker!A:M"
    ).execute()
    
    rows = result.get("values", [])
    if not rows:
        return {"error": "No data found in sheet"}
    
    today = date.today()
    overdue = []
    
    for row in rows[1:]:
        if len(row) < 10:
            continue
        
        next_due = row[9] if len(row) > 9 else ""
        status = row[7] if len(row) > 7 else ""
        
        if status in ("COMPLETED", "N/A"):
            continue
        
        try:
            due_date = date.fromisoformat(next_due)
            if due_date < today:
                overdue.append({
                    "id": row[0],
                    "item": row[1],
                    "category": row[2],
                    "deadline": next_due,
                    "days_overdue": (today - due_date).days,
                    "form": row[6] if len(row) > 6 else "",
                    "status": status,
                    "risk": row[12] if len(row) > 12 else "",
                    "penalty_risk": "CRITICAL" if (today - due_date).days > 30 else "HIGH"
                })
        except (ValueError, IndexError):
            continue
    
    overdue.sort(key=lambda x: x["days_overdue"], reverse=True)
    
    return {
        "query": "Overdue compliance items",
        "generated_at": datetime.now().isoformat(),
        "today": today.isoformat(),
        "count": len(overdue),
        "items": overdue,
        "alert": f"⚠ {len(overdue)} overdue items requiring immediate attention!" if overdue else "✓ No overdue items"
    }


def update_status(sheet_id: str, item_id: str, status: str,
                  completion_date: str = None, notes: str = None) -> dict:
    """Update the status of a compliance item in the tracker."""
    service = get_sheets_service()
    sheet = service.spreadsheets()
    
    # Read current data
    result = sheet.values().get(
        spreadsheetId=sheet_id,
        range="Compliance Tracker!A:M"
    ).execute()
    
    rows = result.get("values", [])
    if not rows:
        return {"error": "No data found in sheet"}
    
    # Find the item
    target_row = None
    for i, row in enumerate(rows):
        if row and row[0] == item_id:
            target_row = i + 1  # 1-indexed for Sheets API
            break
    
    if not target_row:
        return {"error": f"Item '{item_id}' not found in tracker"}
    
    # Update status (column H = index 8)
    updates = []
    updates.append({
        "range": f"Compliance Tracker!H{target_row}",
        "values": [[status.upper()]]
    })
    
    # Update last completed date (column I = index 9)
    if completion_date:
        updates.append({
            "range": f"Compliance Tracker!I{target_row}",
            "values": [[completion_date]]
        })
    
    # Update notes (column L = index 12)
    if notes:
        updates.append({
            "range": f"Compliance Tracker!L{target_row}",
            "values": [[notes]]
        })
    
    # Batch update
    body = {"valueInputOption": "USER_ENTERED", "data": updates}
    sheet.values().batchUpdate(spreadsheetId=sheet_id, body=body).execute()
    
    return {
        "updated": True,
        "item_id": item_id,
        "new_status": status.upper(),
        "completion_date": completion_date,
        "notes": notes,
        "timestamp": datetime.now().isoformat()
    }


def main():
    parser = argparse.ArgumentParser(description="Indian Legal Compliance Tracker")
    parser.add_argument("--mode", required=True,
                       choices=["init", "upcoming", "overdue", "update"],
                       help="Operation mode")
    parser.add_argument("--company", help="Company name (for init)")
    parser.add_argument("--checklist", help="Path to compliance checklist JSON (for init)")
    parser.add_argument("--sheet-id", help="Google Sheet ID for tracking")
    parser.add_argument("--days", type=int, default=30, help="Days ahead to check (for upcoming)")
    parser.add_argument("--item-id", help="Compliance item ID (for update)")
    parser.add_argument("--status", help="New status (for update): completed, in_progress, pending, not_started")
    parser.add_argument("--date", help="Completion date YYYY-MM-DD (for update)")
    parser.add_argument("--notes", help="Notes to add (for update)")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--copilot", action="store_true",
                       help="Copilot mode — output analysis prompt")
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"COMPLIANCE TRACKER — Mode: {args.mode}")
    print(f"{'='*60}")
    
    if args.mode == "init":
        if not args.checklist:
            print("ERROR: --checklist is required for init mode")
            sys.exit(1)
        if not Path(args.checklist).exists():
            print(f"ERROR: Checklist file not found: {args.checklist}")
            sys.exit(1)
        
        result = init_tracker(args.company or "Company", args.checklist, args.sheet_id)
    
    elif args.mode == "upcoming":
        if not args.sheet_id:
            print("ERROR: --sheet-id is required for upcoming mode")
            print("Tip: First run --mode init to create the tracker")
            sys.exit(1)
        result = get_upcoming(args.sheet_id, args.days)
    
    elif args.mode == "overdue":
        if not args.sheet_id:
            print("ERROR: --sheet-id is required for overdue mode")
            sys.exit(1)
        result = get_overdue(args.sheet_id)
    
    elif args.mode == "update":
        if not all([args.sheet_id, args.item_id, args.status]):
            print("ERROR: --sheet-id, --item-id, and --status are required for update mode")
            sys.exit(1)
        result = update_status(args.sheet_id, args.item_id, args.status, args.date, args.notes)
    
    # Save output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n✓ Results saved to {output_path}")
    
    if args.mode == "init":
        print(f"  Total items tracked: {result.get('total_items', 0)}")
    elif args.mode == "upcoming":
        print(f"  Items due in {args.days} days: {result.get('count', 0)}")
    elif args.mode == "overdue":
        print(f"  Overdue items: {result.get('count', 0)}")
    elif args.mode == "update":
        print(f"  Updated: {args.item_id} → {args.status}")
    
    if args.copilot:
        print(f"\n{'='*60}")
        print("COPILOT MODE:")
        print(f"{'='*60}")
        if args.mode in ("upcoming", "overdue"):
            print(f"Review the {args.mode} compliance items in {output_path}.")
            print("For each item, provide:")
            print("1. Priority and urgency assessment")
            print("2. Required actions and responsible persons")
            print("3. Estimated time/cost to complete")
            print("4. Consequences of non-compliance")
    
    return result


if __name__ == "__main__":
    main()
