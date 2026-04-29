#!/usr/bin/env python3
"""
Candidate / People Research Tool.

Searches the web for information about candidates using SerpAPI.
Also supports salary benchmarking for roles.

Usage:
    python research_candidate.py --name "John Doe" --current-company "Acme Corp"
    python research_candidate.py --name "Jane Smith" --role "Mechanical Engineer" --output .tmp/research/
    python research_candidate.py --mode salary-benchmark --role "Embedded Systems Engineer" --location "Bangalore"
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

RATE_LIMIT_DELAY = 2.0


def serpapi_search(query: str, num_results: int = 10, engine: str = "google") -> dict:
    """Execute a SerpAPI search."""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError(
            "SERPAPI_API_KEY not set. Get one at https://serpapi.com/ "
            "(free tier: 100 searches/month)"
        )

    params = {
        "engine": engine,
        "q": query,
        "api_key": api_key,
        "num": num_results,
    }
    time.sleep(RATE_LIMIT_DELAY)
    resp = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def research_person(name: str, current_company: str = None,
                    role: str = None, location: str = None) -> dict:
    """
    Research a person online using multiple search queries.
    Returns structured findings.
    """
    print(f"  Researching: {name}")
    findings = {
        "name": name,
        "current_company": current_company,
        "role": role,
        "linkedin": [],
        "github": [],
        "publications": [],
        "news": [],
        "other": [],
        "searched_at": datetime.now().isoformat()
    }

    queries = []
    base = f'"{name}"'
    if current_company:
        base += f' "{current_company}"'

    queries.append(f'{base} LinkedIn')
    queries.append(f'{base} site:github.com OR site:gitlab.com')
    if role:
        queries.append(f'{base} {role}')

    for query in queries:
        try:
            results = serpapi_search(query, num_results=5)
            organic = results.get("organic_results", [])
            for r in organic:
                entry = {
                    "title": r.get("title", ""),
                    "link": r.get("link", ""),
                    "snippet": r.get("snippet", ""),
                }
                link = entry["link"].lower()
                if "linkedin.com" in link:
                    findings["linkedin"].append(entry)
                elif "github.com" in link or "gitlab.com" in link:
                    findings["github"].append(entry)
                elif any(s in link for s in ["scholar.google", "researchgate", "arxiv"]):
                    findings["publications"].append(entry)
                else:
                    findings["other"].append(entry)
        except Exception as e:
            print(f"  Warning: Search failed for '{query}': {e}")

    # Deduplicate by link
    for key in ["linkedin", "github", "publications", "other"]:
        seen_links = set()
        unique = []
        for item in findings[key]:
            if item["link"] not in seen_links:
                seen_links.add(item["link"])
                unique.append(item)
        findings[key] = unique

    return findings


def salary_benchmark(role: str, location: str = "Bangalore, India",
                     level: str = None) -> dict:
    """
    Search for salary benchmarks for a role using SerpAPI.
    Returns structured salary data from search results.
    """
    print(f"  Benchmarking salary: {role} in {location}")
    queries = [
        f"{role} salary {location} 2025 2026",
        f"{role} average salary India CTC package",
    ]
    if level:
        queries.append(f"{level} {role} salary {location}")

    results_all = []
    for query in queries:
        try:
            results = serpapi_search(query, num_results=5)
            for r in results.get("organic_results", []):
                results_all.append({
                    "title": r.get("title", ""),
                    "link": r.get("link", ""),
                    "snippet": r.get("snippet", ""),
                })
        except Exception as e:
            print(f"  Warning: Salary search failed: {e}")

    return {
        "role": role,
        "location": location,
        "level": level,
        "search_results": results_all,
        "note": "These are web search results. Extract salary ranges from snippets. Figures are approximate market estimates.",
        "searched_at": datetime.now().isoformat()
    }


def format_research_report(findings: dict) -> str:
    """Format research findings as readable text."""
    text = f"\n{'='*60}\n"
    text += f"CANDIDATE RESEARCH REPORT\n"
    text += f"{'='*60}\n\n"
    text += f"Name:    {findings.get('name', 'N/A')}\n"
    text += f"Company: {findings.get('current_company', 'N/A')}\n"
    text += f"Role:    {findings.get('role', 'N/A')}\n\n"

    if findings["linkedin"]:
        text += "--- LinkedIn Profiles ---\n"
        for item in findings["linkedin"][:3]:
            text += f"  {item['title']}\n  {item['link']}\n  {item.get('snippet', '')[:150]}\n\n"

    if findings["github"]:
        text += "--- GitHub / Code Profiles ---\n"
        for item in findings["github"][:3]:
            text += f"  {item['title']}\n  {item['link']}\n  {item.get('snippet', '')[:150]}\n\n"

    if findings["publications"]:
        text += "--- Publications / Academic ---\n"
        for item in findings["publications"][:3]:
            text += f"  {item['title']}\n  {item['link']}\n  {item.get('snippet', '')[:150]}\n\n"

    if findings["other"]:
        text += "--- Other Mentions ---\n"
        for item in findings["other"][:5]:
            text += f"  {item['title']}\n  {item['link']}\n  {item.get('snippet', '')[:150]}\n\n"

    total = sum(len(findings[k]) for k in ["linkedin", "github", "publications", "other"])
    text += f"Total results found: {total}\n"
    text += f"{'='*60}\n"
    return text


def main():
    parser = argparse.ArgumentParser(description="Research candidates or benchmark salaries")
    parser.add_argument("--mode", default="person", choices=["person", "salary-benchmark"],
                        help="Research mode")
    parser.add_argument("--name", help="Candidate name (for person mode)")
    parser.add_argument("--current-company", help="Current company (for person mode)")
    parser.add_argument("--role", help="Role title")
    parser.add_argument("--location", default="Bangalore, India", help="Location")
    parser.add_argument("--level", help="Seniority level (for salary-benchmark)")
    parser.add_argument("--output", default=".tmp/research/", help="Output directory")
    parser.add_argument("--copilot", action="store_true",
                        help="Output prompt for Copilot synthesis")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "salary-benchmark":
        if not args.role:
            print("ERROR: --role required for salary-benchmark mode")
            sys.exit(1)
        result = salary_benchmark(args.role, args.location, args.level)
        out_file = output_dir / f"salary_{args.role.lower().replace(' ', '-')}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n  Saved to {out_file}")
        print(f"\n  Found {len(result['search_results'])} results for salary data.")
        for r in result["search_results"][:5]:
            print(f"    - {r['title'][:80]}")
            if r.get("snippet"):
                print(f"      {r['snippet'][:120]}")

        if args.copilot:
            print("\n--- COPILOT SALARY ANALYSIS PROMPT ---")
            print(f"Analyze these salary search results for {args.role} in {args.location}.")
            print(f"Extract salary ranges (min/median/max) in INR LPA and provide a summary.")
            print(json.dumps(result["search_results"], indent=2))
            print("--- END PROMPT ---")

    else:  # person mode
        if not args.name:
            print("ERROR: --name required for person mode")
            sys.exit(1)
        result = research_person(args.name, args.current_company, args.role, args.location)
        slug = args.name.lower().replace(" ", "-")
        out_file = output_dir / f"research_{slug}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(format_research_report(result))
        print(f"  Saved to {out_file}")

        if args.copilot:
            print("\n--- COPILOT SYNTHESIS PROMPT ---")
            print(f"Synthesize this online research about {args.name} into a candidate background brief.")
            print(f"Highlight: professional background, notable projects, publications, red flags.")
            print(json.dumps({k: v for k, v in result.items() if k != "searched_at"}, indent=2))
            print("--- END PROMPT ---")


if __name__ == "__main__":
    main()
