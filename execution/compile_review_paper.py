#!/usr/bin/env python3
"""
Review Paper Compiler

Compiles paper summaries into a structured review paper.
Generates both markdown output and BibTeX references.

Usage:
    python compile_review_paper.py --topic "Machine Learning" --papers ".tmp/discovered_papers.json" --output ".tmp/review_paper.md"
    python compile_review_paper.py --summaries-dir ".tmp/paper_summaries/" --output ".tmp/review_paper.md"
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def load_papers_json(json_path: Path) -> list:
    """Load papers from discovered_papers.json."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("papers", [])


def load_summaries(summaries_dir: Path) -> dict:
    """Load all paper summaries from a directory."""
    summaries = {}
    if not summaries_dir.exists():
        return summaries
    
    for md_file in summaries_dir.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        summaries[md_file.stem] = content
    
    return summaries


def generate_citation_key(paper: dict) -> str:
    """Generate a BibTeX citation key from paper metadata."""
    first_author = ""
    authors = paper.get("authors", [])
    if authors:
        # Get last name of first author
        first_author = authors[0].split()[-1].lower()
        # Remove non-alphanumeric
        first_author = re.sub(r'[^a-z]', '', first_author)
    
    year = paper.get("year", "")
    
    # Get first significant word from title
    title = paper.get("title", "")
    title_word = ""
    for word in title.split():
        if len(word) > 3 and word.lower() not in ["the", "for", "and", "with"]:
            title_word = re.sub(r'[^a-z]', '', word.lower())[:10]
            break
    
    return f"{first_author}{year}{title_word}"


def format_authors_bibtex(authors: list) -> str:
    """Format authors for BibTeX."""
    if not authors:
        return "Unknown"
    return " and ".join(authors)


def format_authors_inline(authors: list) -> str:
    """Format authors for inline citation (Author et al., Year)."""
    if not authors:
        return "Unknown"
    
    first_author = authors[0].split()[-1]  # Last name
    
    if len(authors) == 1:
        return first_author
    elif len(authors) == 2:
        second_author = authors[1].split()[-1]
        return f"{first_author} & {second_author}"
    else:
        return f"{first_author} et al."


def generate_bibtex(papers: list) -> str:
    """Generate BibTeX entries for all papers."""
    entries = []
    seen_keys = set()
    
    for paper in papers:
        key = generate_citation_key(paper)
        
        # Handle duplicate keys
        original_key = key
        counter = 1
        while key in seen_keys:
            key = f"{original_key}{chr(ord('a') + counter - 1)}"
            counter += 1
        seen_keys.add(key)
        
        paper["_citation_key"] = key
        
        doi = paper.get("doi", "")
        year = paper.get("year", "")
        title = paper.get("title", "").replace("{", "\\{").replace("}", "\\}")
        authors = format_authors_bibtex(paper.get("authors", []))
        venue = paper.get("venue", "")
        
        entry = f"""@article{{{key},
  title = {{{title}}},
  author = {{{authors}}},
  year = {{{year}}},
  journal = {{{venue}}},
  doi = {{{doi}}}
}}"""
        entries.append(entry)
    
    return "\n\n".join(entries)


def categorize_papers(papers: list) -> dict:
    """
    Categorize papers by topic/theme based on title and abstract.
    Returns a dict of category -> list of papers.
    """
    # Simple keyword-based categorization
    categories = defaultdict(list)
    
    # Define category keywords
    category_keywords = {
        "Methodology & Techniques": ["method", "technique", "approach", "algorithm", "framework", "model"],
        "Applications": ["application", "system", "tool", "platform", "implementation", "practical"],
        "Theoretical Foundations": ["theory", "theoretical", "foundation", "principle", "formal", "analysis"],
        "Evaluation & Benchmarks": ["evaluation", "benchmark", "comparison", "performance", "assessment", "study"],
        "Surveys & Reviews": ["survey", "review", "overview", "state-of-the-art", "comprehensive"],
    }
    
    for paper in papers:
        title = paper.get("title", "").lower()
        abstract = paper.get("abstract", "").lower() if paper.get("abstract") else ""
        text = f"{title} {abstract}"
        
        categorized = False
        for category, keywords in category_keywords.items():
            if any(kw in text for kw in keywords):
                categories[category].append(paper)
                categorized = True
                break
        
        if not categorized:
            categories["Other Research"].append(paper)
    
    return dict(categories)


def generate_review_structure(topic: str, papers: list, summaries: dict = None) -> str:
    """
    Generate the review paper markdown structure.
    This creates placeholders for Copilot to fill in with actual content.
    """
    today = datetime.now().strftime("%B %d, %Y")
    
    md = []
    
    # Title and metadata
    md.append(f"# State-of-the-Art Review: {topic}")
    md.append("")
    md.append(f"*Generated: {today}*")
    md.append(f"*Papers Reviewed: {len(papers)}*")
    md.append("")
    md.append("---")
    md.append("")
    
    # Abstract
    md.append("## Abstract")
    md.append("")
    md.append("<!-- COPILOT: Write a comprehensive abstract summarizing this review paper. -->")
    md.append("<!-- Include: scope of review, methodology, key findings, and implications -->")
    md.append("")
    md.append("**[Abstract to be written based on the content below]**")
    md.append("")
    
    # Table of Contents
    md.append("## Table of Contents")
    md.append("")
    md.append("1. [Introduction](#introduction)")
    md.append("2. [Methodology](#methodology)")
    md.append("3. [Background](#background)")
    md.append("4. [State of the Art](#state-of-the-art)")
    md.append("5. [Discussion](#discussion)")
    md.append("6. [Conclusion](#conclusion)")
    md.append("7. [References](#references)")
    md.append("")
    
    # Introduction
    md.append("## Introduction")
    md.append("")
    md.append("### Problem Statement")
    md.append("")
    md.append(f"<!-- COPILOT: Write an introduction to {topic}. -->")
    md.append("<!-- Include: What is the research problem? Why is it important? -->")
    md.append("")
    md.append("### Scope of This Review")
    md.append("")
    md.append(f"This review examines {len(papers)} papers published on the topic of **{topic}**.")
    md.append("")
    
    # Year distribution
    years = [p.get("year") for p in papers if p.get("year")]
    if years:
        year_range = f"{min(years)}-{max(years)}"
        md.append(f"**Publication Period:** {year_range}")
    
    # Source distribution
    sources = defaultdict(int)
    for p in papers:
        sources[p.get("source", "unknown")] += 1
    md.append("")
    md.append("**Sources:**")
    for source, count in sorted(sources.items(), key=lambda x: -x[1]):
        md.append(f"- {source.replace('_', ' ').title()}: {count} papers")
    md.append("")
    
    # Methodology section
    md.append("## Methodology")
    md.append("")
    md.append("### Search Strategy")
    md.append("")
    md.append("Papers were collected from multiple academic databases:")
    md.append("- **Semantic Scholar**: Comprehensive academic graph")
    md.append("- **CrossRef**: DOI registration and metadata")
    md.append("- **arXiv**: Preprint repository")
    md.append("- **Google Scholar**: General academic search")
    md.append("")
    md.append("### Selection Criteria")
    md.append("")
    md.append("Papers were selected based on:")
    md.append("1. Relevance to the topic")
    md.append("2. Citation count (influence in the field)")
    md.append("3. Publication recency (state-of-the-art)")
    md.append("4. Availability (open access preferred)")
    md.append("")
    
    # Background
    md.append("## Background")
    md.append("")
    md.append("<!-- COPILOT: Write background section covering foundational concepts -->")
    md.append("<!-- Include: Key definitions, historical context, fundamental theories -->")
    md.append("")
    md.append("**[Background to be synthesized from the papers below]**")
    md.append("")
    
    # State of the Art - categorized
    md.append("## State of the Art")
    md.append("")
    
    categories = categorize_papers(papers)
    
    for category, cat_papers in categories.items():
        md.append(f"### {category}")
        md.append("")
        md.append(f"*{len(cat_papers)} papers in this category*")
        md.append("")
        
        for paper in cat_papers[:10]:  # Limit per category
            title = paper.get("title", "Unknown")
            authors = format_authors_inline(paper.get("authors", []))
            year = paper.get("year", "?")
            doi = paper.get("doi")
            citation_key = paper.get("_citation_key", "")
            
            md.append(f"#### {title}")
            md.append("")
            md.append(f"**Authors:** {', '.join(paper.get('authors', ['Unknown'])[:5])}")
            if len(paper.get("authors", [])) > 5:
                md.append(f" *et al.*")
            md.append("")
            md.append(f"**Year:** {year}")
            if doi:
                md.append(f"**DOI:** [{doi}](https://doi.org/{doi})")
            md.append("")
            
            # Include abstract if available
            abstract = paper.get("abstract")
            if abstract:
                md.append("**Abstract:**")
                md.append(f"> {abstract[:500]}..." if len(abstract) > 500 else f"> {abstract}")
                md.append("")
            
            # Check if we have a summary
            summary_key = citation_key or sanitize_for_filename(title)
            if summaries and summary_key in summaries:
                md.append("**Summary:**")
                md.append(summaries[summary_key])
                md.append("")
            else:
                md.append("<!-- COPILOT: Summarize this paper's key contributions -->")
                md.append("")
            
            md.append(f"*Citation: ({authors}, {year})[^{citation_key}]*")
            md.append("")
            md.append("---")
            md.append("")
    
    # Discussion
    md.append("## Discussion")
    md.append("")
    md.append("### Key Themes and Trends")
    md.append("")
    md.append("<!-- COPILOT: Identify and discuss major themes across the reviewed papers -->")
    md.append("")
    md.append("### Comparison of Approaches")
    md.append("")
    md.append("<!-- COPILOT: Compare different methodologies and their trade-offs -->")
    md.append("")
    md.append("### Research Gaps")
    md.append("")
    md.append("<!-- COPILOT: Identify gaps in the current research landscape -->")
    md.append("")
    md.append("### Future Directions")
    md.append("")
    md.append("<!-- COPILOT: Suggest promising directions for future research -->")
    md.append("")
    
    # Conclusion
    md.append("## Conclusion")
    md.append("")
    md.append("<!-- COPILOT: Write a conclusion summarizing key findings and implications -->")
    md.append("")
    
    # References
    md.append("## References")
    md.append("")
    
    for paper in papers:
        key = paper.get("_citation_key", "")
        authors = format_authors_inline(paper.get("authors", []))
        year = paper.get("year", "?")
        title = paper.get("title", "Unknown")
        venue = paper.get("venue", "")
        doi = paper.get("doi")
        
        ref_line = f"[^{key}]: {authors} ({year}). *{title}*."
        if venue:
            ref_line += f" {venue}."
        if doi:
            ref_line += f" DOI: [{doi}](https://doi.org/{doi})"
        
        md.append(ref_line)
        md.append("")
    
    return "\n".join(md)


def sanitize_for_filename(s: str) -> str:
    """Convert string to safe filename."""
    safe = re.sub(r'[^a-zA-Z0-9]', '_', s.lower())
    return re.sub(r'_+', '_', safe)[:50]


def main():
    parser = argparse.ArgumentParser(description="Compile review paper from paper data")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--papers", required=True, help="Path to discovered_papers.json")
    parser.add_argument("--summaries-dir", help="Directory containing paper summaries")
    parser.add_argument("--output", default=".tmp/review_paper.md", help="Output markdown file")
    parser.add_argument("--bibtex", default=".tmp/references.bib", help="Output BibTeX file")
    
    args = parser.parse_args()
    
    # Load papers
    papers_path = Path(args.papers)
    if not papers_path.exists():
        print(f"Error: Papers file not found: {papers_path}")
        sys.exit(1)
    
    papers = load_papers_json(papers_path)
    print(f"Loaded {len(papers)} papers")
    
    # Load summaries if available
    summaries = {}
    if args.summaries_dir:
        summaries_dir = Path(args.summaries_dir)
        summaries = load_summaries(summaries_dir)
        print(f"Loaded {len(summaries)} paper summaries")
    
    # Generate BibTeX
    print("Generating BibTeX references...")
    bibtex = generate_bibtex(papers)
    bibtex_path = Path(args.bibtex)
    bibtex_path.parent.mkdir(parents=True, exist_ok=True)
    with open(bibtex_path, "w", encoding="utf-8") as f:
        f.write(bibtex)
    print(f"BibTeX saved to: {bibtex_path}")
    
    # Generate review structure
    print("Generating review paper structure...")
    review = generate_review_structure(args.topic, papers, summaries)
    
    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(review)
    
    print(f"\nReview paper saved to: {output_path}")
    print(f"BibTeX references saved to: {bibtex_path}")
    print("\nNext steps:")
    print("1. Review and edit the generated structure")
    print("2. Ask Copilot to fill in the <!-- COPILOT: ... --> sections")
    print("3. Add paper summaries for richer content")


if __name__ == "__main__":
    main()
