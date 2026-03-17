#!/usr/bin/env python3
"""
Indian Legal Research Tool

Searches Indian legal databases, acts, case law, and government notifications.
Uses publicly available sources — no API key required.

Sources:
  - Indian Kanoon (case law + acts)
  - legislative.gov.in (Central acts)
  - MCA portal (company law)
  - India Code (consolidated acts)

Usage:
    python legal_research.py --mode search --query "maternity benefit act 2017 amendment" --output .tmp/results.json
    python legal_research.py --mode act_lookup --act "Companies Act 2013" --section "149" --output .tmp/section.json
    python legal_research.py --mode case_law --query "non-compete clause enforceability India" --output .tmp/cases.json
    python legal_research.py --mode notification --query "labor code gazette notification 2024" --output .tmp/notifications.json
"""

import os
import sys
import json
import argparse
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus, urljoin

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Constants
INDIAN_KANOON_BASE = "https://indiankanoon.org"
INDIA_CODE_BASE = "https://www.indiacode.nic.in"
LEGISLATIVE_BASE = "https://legislative.gov.in"

# User agent for requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Mapping of common act names to their Indian Kanoon search terms
COMMON_ACTS = {
    "companies act": "Companies Act, 2013",
    "companies act 2013": "Companies Act, 2013",
    "indian contract act": "Indian Contract Act, 1872",
    "contract act": "Indian Contract Act, 1872",
    "trade marks act": "Trade Marks Act, 1999",
    "trademarks act": "Trade Marks Act, 1999",
    "patents act": "Patents Act, 1970",
    "copyright act": "Copyright Act, 1957",
    "it act": "Information Technology Act, 2000",
    "posh act": "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
    "maternity benefit act": "Maternity Benefit Act, 1961",
    "payment of gratuity act": "Payment of Gratuity Act, 1972",
    "gratuity act": "Payment of Gratuity Act, 1972",
    "epf act": "Employees' Provident Funds and Miscellaneous Provisions Act, 1952",
    "esi act": "Employees' State Insurance Act, 1948",
    "minimum wages act": "Minimum Wages Act, 1948",
    "payment of wages act": "Payment of Wages Act, 1936",
    "industrial disputes act": "Industrial Disputes Act, 1947",
    "factories act": "Factories Act, 1948",
    "shops and establishments act": "Shops and Establishments Act",
    "negotiable instruments act": "Negotiable Instruments Act, 1881",
    "arbitration act": "Arbitration and Conciliation Act, 1996",
    "specific relief act": "Specific Relief Act, 1963",
    "stamp act": "Indian Stamp Act, 1899",
    "gst act": "Central Goods and Services Tax Act, 2017",
    "cgst act": "Central Goods and Services Tax Act, 2017",
    "igst act": "Integrated Goods and Services Tax Act, 2017",
    "income tax act": "Income Tax Act, 1961",
    "contract labour act": "Contract Labour (Regulation and Abolition) Act, 1970",
    "code on wages": "Code on Wages, 2019",
    "code on social security": "Code on Social Security, 2020",
    "industrial relations code": "Industrial Relations Code, 2020",
    "osh code": "Occupational Safety, Health and Working Conditions Code, 2020",
    "designs act": "Designs Act, 2000",
    "dpdp act": "Digital Personal Data Protection Act, 2023",
    "equal remuneration act": "Equal Remuneration Act, 1976",
}


def search_indian_kanoon(query: str, max_results: int = 10) -> list:
    """
    Search Indian Kanoon for case law, acts, and legal resources.
    Returns a list of results with title, snippet, and URL.
    """
    results = []
    try:
        search_url = f"{INDIAN_KANOON_BASE}/search/?formInput={quote_plus(query)}"
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        
        # Parse results from HTML (basic extraction)
        html = resp.text
        
        # Extract result entries - Indian Kanoon uses <div class="result"> pattern
        result_blocks = re.findall(
            r'<div class="result"[^>]*>(.*?)</div>\s*(?=<div class="result"|<div class="pagination")',
            html, re.DOTALL
        )
        
        if not result_blocks:
            # Alternative pattern
            result_blocks = re.findall(
                r'<div class="result_title">(.*?)</div>.*?<div class="result_text">(.*?)</div>',
                html, re.DOTALL
            )
        
        # Extract title and link from result blocks
        for i, block in enumerate(result_blocks[:max_results]):
            title_match = re.search(r'<a href="(/doc/\d+/[^"]*)"[^>]*>(.*?)</a>', block)
            if title_match:
                link = INDIAN_KANOON_BASE + title_match.group(1)
                title = re.sub(r'<[^>]+>', '', title_match.group(2)).strip()
                snippet = re.sub(r'<[^>]+>', '', block).strip()[:300]
                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet,
                    "source": "Indian Kanoon"
                })
        
        # If regex parsing didn't work well, create a general result
        if not results:
            results.append({
                "title": f"Search results for: {query}",
                "url": search_url,
                "snippet": "Visit Indian Kanoon directly for detailed results. The search was performed but automated extraction needs the page structure.",
                "source": "Indian Kanoon",
                "note": "Open the URL in browser for full results"
            })

    except requests.RequestException as e:
        results.append({
            "title": f"Search: {query}",
            "url": f"{INDIAN_KANOON_BASE}/search/?formInput={quote_plus(query)}",
            "snippet": f"Could not fetch results automatically: {str(e)}. Visit the URL manually.",
            "source": "Indian Kanoon",
            "error": str(e)
        })
    
    return results


def search_serpapi(query: str, max_results: int = 10) -> list:
    """
    Use SerpAPI for Google search if API key is available.
    Falls back gracefully if not available.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return []
    
    results = []
    try:
        params = {
            "q": query + " site:indiankanoon.org OR site:legislative.gov.in OR site:mca.gov.in OR site:indiacode.nic.in",
            "api_key": api_key,
            "num": max_results,
            "gl": "in",
            "hl": "en"
        }
        resp = requests.get("https://serpapi.com/search", params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        for r in data.get("organic_results", [])[:max_results]:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("link", ""),
                "snippet": r.get("snippet", ""),
                "source": "Google (SerpAPI)"
            })
    except Exception as e:
        print(f"  ⚠ SerpAPI search failed: {e}")
    
    return results


def lookup_act(act_name: str, section: str = None) -> dict:
    """
    Look up a specific act and optionally a specific section.
    """
    # Normalize act name
    normalized = act_name.lower().strip()
    full_name = COMMON_ACTS.get(normalized, act_name)
    
    result = {
        "act": full_name,
        "section": section,
        "sources": [],
        "content": None
    }
    
    # Search Indian Kanoon for the act/section
    if section:
        query = f'"{full_name}" section {section}'
    else:
        query = f'"{full_name}"'
    
    kanoon_results = search_indian_kanoon(query, max_results=5)
    result["sources"].extend(kanoon_results)
    
    # Also try SerpAPI if available
    serp_results = search_serpapi(f"{full_name} section {section}" if section else full_name, max_results=5)
    result["sources"].extend(serp_results)
    
    # Build India Code URL
    india_code_search = f"{INDIA_CODE_BASE}/handle/123456789/1362?sam_handle=123456789/1362"
    result["india_code_url"] = india_code_search
    
    # Build Indian Kanoon direct URL
    kanoon_search = f"{INDIAN_KANOON_BASE}/search/?formInput={quote_plus(query)}"
    result["kanoon_url"] = kanoon_search
    
    return result


def search_case_law(query: str, max_results: int = 10) -> list:
    """
    Search for case law on Indian Kanoon.
    """
    # Add court filters for better results
    enhanced_query = f"{query} doctypes: supremecourt,highcourt"
    results = search_indian_kanoon(enhanced_query, max_results)
    
    # Also try SerpAPI
    serp_results = search_serpapi(f"{query} Indian case law judgment", max_results=5)
    results.extend(serp_results)
    
    return results


def search_notifications(query: str, max_results: int = 10) -> list:
    """
    Search for government notifications, circulars, and gazette entries.
    """
    results = []
    
    # Search for gazette notifications
    serp_results = search_serpapi(
        f"{query} site:egazette.nic.in OR site:mca.gov.in OR site:labour.gov.in OR site:dpiit.gov.in",
        max_results=max_results
    )
    results.extend(serp_results)
    
    # Also search Indian Kanoon for notifications
    kanoon_results = search_indian_kanoon(f"{query} notification circular", max_results=5)
    results.extend(kanoon_results)
    
    # Add direct portal links
    results.append({
        "title": "MCA Notifications & Circulars",
        "url": "https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/acts.html",
        "snippet": "Ministry of Corporate Affairs — Official notifications, circulars, and rules",
        "source": "Direct Portal"
    })
    results.append({
        "title": "Labour Ministry Notifications",
        "url": "https://labour.gov.in/lcandilaw/labour-law-reforms",
        "snippet": "Ministry of Labour & Employment — Labour law reforms and notifications",
        "source": "Direct Portal"
    })
    results.append({
        "title": "eGazette of India",
        "url": "https://egazette.gov.in/",
        "snippet": "Official Gazette of India — All government notifications",
        "source": "Direct Portal"
    })
    
    return results


def format_results(mode: str, query: str, results: list | dict, area: str = None) -> dict:
    """Format the output with metadata."""
    return {
        "mode": mode,
        "query": query,
        "area_of_law": area,
        "timestamp": datetime.now().isoformat(),
        "result_count": len(results) if isinstance(results, list) else 1,
        "results": results,
        "disclaimer": "This information is for reference only and does not constitute legal advice. "
                      "Please consult a qualified Indian legal professional for specific guidance.",
        "sources_note": "Results sourced from Indian Kanoon, India Code, and government portals. "
                       "SerpAPI used if SERPAPI_API_KEY is configured."
    }


def main():
    parser = argparse.ArgumentParser(description="Indian Legal Research Tool")
    parser.add_argument("--mode", required=True, choices=["search", "act_lookup", "case_law", "notification"],
                       help="Research mode")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--act", help="Act name for lookup (e.g., 'Companies Act 2013')")
    parser.add_argument("--section", help="Section number for act lookup")
    parser.add_argument("--area", help="Area of law (hr, labor, company, ip, contract, tax)")
    parser.add_argument("--max-results", type=int, default=10, help="Maximum results to return")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--copilot", action="store_true",
                       help="Copilot mode — output prompt for Copilot to process results")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"INDIAN LEGAL RESEARCH — Mode: {args.mode}")
    print(f"{'='*60}")
    
    if args.mode == "search":
        if not args.query:
            print("ERROR: --query is required for search mode")
            sys.exit(1)
        print(f"Query: {args.query}")
        if args.area:
            print(f"Area: {args.area}")
        
        # Search multiple sources
        all_results = []
        print("  Searching Indian Kanoon...")
        all_results.extend(search_indian_kanoon(args.query, args.max_results))
        
        print("  Searching via SerpAPI (if configured)...")
        all_results.extend(search_serpapi(args.query + " Indian law", args.max_results // 2))
        
        output = format_results("search", args.query, all_results, args.area)
    
    elif args.mode == "act_lookup":
        act = args.act or args.query
        if not act:
            print("ERROR: --act or --query is required for act_lookup mode")
            sys.exit(1)
        print(f"Act: {act}")
        if args.section:
            print(f"Section: {args.section}")
        
        result = lookup_act(act, args.section)
        output = format_results("act_lookup", f"{act} section {args.section}" if args.section else act, result)
    
    elif args.mode == "case_law":
        if not args.query:
            print("ERROR: --query is required for case_law mode")
            sys.exit(1)
        print(f"Query: {args.query}")
        
        results = search_case_law(args.query, args.max_results)
        output = format_results("case_law", args.query, results)
    
    elif args.mode == "notification":
        if not args.query:
            print("ERROR: --query is required for notification mode")
            sys.exit(1)
        print(f"Query: {args.query}")
        
        results = search_notifications(args.query, args.max_results)
        output = format_results("notification", args.query, results)
    
    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to {output_path}")
    print(f"  Found {output['result_count']} result(s)")
    
    if args.copilot:
        print(f"\n{'='*60}")
        print("COPILOT MODE — Process these results:")
        print(f"{'='*60}")
        print(f"\nPlease analyze the research results in {output_path}.")
        print("Synthesize the findings into a clear legal memo covering:")
        print("1. Applicable law/regulation and relevant sections")
        print("2. Key requirements and obligations")
        print("3. Recent amendments or notifications")
        print("4. Practical implications and recommendations")
        print("5. Add standard legal disclaimer")
    
    return output


if __name__ == "__main__":
    main()
