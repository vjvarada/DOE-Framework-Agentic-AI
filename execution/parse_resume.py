#!/usr/bin/env python3
"""
Resume Parser - Extract structured data from PDF resumes.

Uses multiple PDF extraction backends (PyMuPDF, pdfplumber, pypdf) for robustness.
Outputs structured JSON with candidate information.

Usage:
    python parse_resume.py --input resume.pdf --output .tmp/parsed/
    python parse_resume.py --input .tmp/resumes/ --output .tmp/parsed/ --batch
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional


def extract_text_pymupdf(pdf_path: Path) -> Optional[str]:
    """Extract text using PyMuPDF (fitz)."""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        pages = []
        for page in doc:
            text = page.get_text("text")
            if text.strip():
                pages.append(text)
        doc.close()
        return "\n\n".join(pages) if pages else None
    except ImportError:
        return None
    except Exception as e:
        print(f"  PyMuPDF failed: {e}")
        return None


def extract_text_pdfplumber(pdf_path: Path) -> Optional[str]:
    """Extract text using pdfplumber."""
    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
        return "\n\n".join(pages) if pages else None
    except ImportError:
        return None
    except Exception as e:
        print(f"  pdfplumber failed: {e}")
        return None


def extract_text_pypdf(pdf_path: Path) -> Optional[str]:
    """Extract text using pypdf."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text and text.strip():
                pages.append(text)
        return "\n\n".join(pages) if pages else None
    except ImportError:
        return None
    except Exception as e:
        print(f"  pypdf failed: {e}")
        return None


def extract_text(pdf_path: Path) -> Optional[str]:
    """Try multiple backends to extract text from PDF."""
    for extractor in [extract_text_pymupdf, extract_text_pdfplumber, extract_text_pypdf]:
        text = extractor(pdf_path)
        if text and len(text.strip()) > 50:
            return text
    return None


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    patterns = [
        r'(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}',  # Indian mobile
        r'(?:\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}',  # International
        r'\d{10,12}',  # Plain digits
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()
    return None


def extract_linkedin(text: str) -> Optional[str]:
    """Extract LinkedIn profile URL from text."""
    pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_github(text: str) -> Optional[str]:
    """Extract GitHub profile URL from text."""
    pattern = r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_skills_section(text: str) -> list:
    """Extract skills from common resume skill sections."""
    skills = []
    # Look for skills section
    skill_patterns = [
        r'(?:technical\s+)?skills?\s*[:\-–]\s*(.*?)(?:\n\n|\n[A-Z])',
        r'(?:core\s+)?competencies\s*[:\-–]\s*(.*?)(?:\n\n|\n[A-Z])',
        r'technologies\s*[:\-–]\s*(.*?)(?:\n\n|\n[A-Z])',
    ]
    for pattern in skill_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            skill_text = match.group(1)
            # Split by common delimiters
            for skill in re.split(r'[,;|•·▪►\n]', skill_text):
                skill = skill.strip().strip('-').strip('•').strip()
                if skill and len(skill) > 1 and len(skill) < 60:
                    skills.append(skill)
    return list(set(skills))


def extract_education(text: str) -> list:
    """Extract education entries from resume text."""
    education = []
    degree_patterns = [
        r'((?:B\.?(?:Tech|E|Sc|A|Com|Arch)|M\.?(?:Tech|E|Sc|A|Com|BA|CA)|Ph\.?D|MBA|BBA|BCA|MCA|Diploma)[^,\n]*)',
        r'((?:Bachelor|Master|Doctor)\s+(?:of|in)\s+[A-Za-z\s]+)',
    ]
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            clean = match.strip()
            if clean and len(clean) > 3:
                education.append(clean)
    return list(set(education))


def extract_experience_years(text: str) -> Optional[float]:
    """Estimate total years of experience from resume text."""
    patterns = [
        r'(\d+\.?\d*)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
        r'(?:experience|exp)\s*[:\-–]\s*(\d+\.?\d*)\+?\s*(?:years?|yrs?)',
        r'total\s+(?:experience|exp)\s*[:\-–]?\s*(\d+\.?\d*)\+?\s*(?:years?|yrs?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None


def parse_resume(pdf_path: Path) -> dict:
    """
    Parse a PDF resume and extract structured data.

    Returns dict with: name, email, phone, linkedin, github, skills,
    education, experience_years, raw_text, word_count, parse_quality
    """
    print(f"  Parsing: {pdf_path.name}")

    text = extract_text(pdf_path)
    if not text:
        return {
            "file": pdf_path.name,
            "error": "Could not extract text from PDF (may be image-based/scanned)",
            "parse_quality": "failed",
            "parsed_at": datetime.now().isoformat()
        }

    # Extract first few lines for name detection
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    # Heuristic: name is usually in first 3 non-empty lines, and is short
    candidate_name = None
    for line in lines[:5]:
        # Skip lines that look like headers, emails, phones, URLs
        if re.search(r'@|http|www\.|resume|curriculum|vitae|\d{5,}', line, re.IGNORECASE):
            continue
        if len(line) < 50 and re.match(r'^[A-Za-z\s.\'-]+$', line):
            candidate_name = line.strip()
            break

    email = extract_email(text)
    phone = extract_phone(text)
    linkedin = extract_linkedin(text)
    github = extract_github(text)
    skills = extract_skills_section(text)
    education = extract_education(text)
    experience_years = extract_experience_years(text)
    word_count = len(text.split())

    # Determine parse quality
    fields_found = sum(1 for x in [candidate_name, email, phone, skills, education] if x)
    if fields_found >= 4:
        quality = "good"
    elif fields_found >= 2:
        quality = "partial"
    else:
        quality = "minimal"

    return {
        "file": pdf_path.name,
        "name": candidate_name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "skills": skills,
        "education": education,
        "experience_years": experience_years,
        "word_count": word_count,
        "parse_quality": quality,
        "raw_text": text,
        "parsed_at": datetime.now().isoformat()
    }


def main():
    parser = argparse.ArgumentParser(description="Parse PDF resumes into structured JSON")
    parser.add_argument("--input", required=True, help="Path to PDF file or directory of PDFs")
    parser.add_argument("--output", default=".tmp/parsed/", help="Output directory for JSON files")
    parser.add_argument("--batch", action="store_true", help="Process all PDFs in directory")
    parser.add_argument("--copilot", action="store_true",
                        help="Output structured prompt for Copilot to analyze")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.batch or input_path.is_dir():
        if not input_path.is_dir():
            print(f"ERROR: {input_path} is not a directory")
            sys.exit(1)
        pdfs = list(input_path.glob("*.pdf"))
        if not pdfs:
            print(f"No PDF files found in {input_path}")
            sys.exit(1)
        print(f"Found {len(pdfs)} PDF(s) to parse")

        results = []
        for pdf in sorted(pdfs):
            result = parse_resume(pdf)
            results.append(result)
            # Save individual JSON
            out_file = output_dir / f"{pdf.stem}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"    → {out_file}")

        # Save summary
        summary_file = output_dir / "_summary.json"
        summary = {
            "total": len(results),
            "successful": sum(1 for r in results if r.get("parse_quality") != "failed"),
            "failed": sum(1 for r in results if r.get("parse_quality") == "failed"),
            "candidates": [
                {
                    "file": r["file"],
                    "name": r.get("name"),
                    "email": r.get("email"),
                    "experience_years": r.get("experience_years"),
                    "skills_count": len(r.get("skills", [])),
                    "parse_quality": r.get("parse_quality")
                }
                for r in results
            ],
            "parsed_at": datetime.now().isoformat()
        }
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"\nSummary saved to {summary_file}")
        print(json.dumps(summary, indent=2))

    else:
        if not input_path.exists():
            print(f"ERROR: File not found: {input_path}")
            sys.exit(1)
        result = parse_resume(input_path)
        out_file = output_dir / f"{input_path.stem}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"  → Saved to {out_file}")

        if args.copilot:
            # Output prompt for Copilot to analyze
            copilot_data = {k: v for k, v in result.items() if k != "raw_text"}
            print("\n--- COPILOT ANALYSIS PROMPT ---")
            print(f"Analyze this parsed resume data and provide a detailed candidate summary:\n")
            print(json.dumps(copilot_data, indent=2))
            print(f"\nFull resume text ({result.get('word_count', 0)} words) available in: {out_file}")
            print("--- END PROMPT ---")
        else:
            # Print summary
            print(f"\n  Name: {result.get('name', 'N/A')}")
            print(f"  Email: {result.get('email', 'N/A')}")
            print(f"  Phone: {result.get('phone', 'N/A')}")
            print(f"  Experience: {result.get('experience_years', 'N/A')} years")
            print(f"  Skills: {len(result.get('skills', []))} found")
            print(f"  Education: {result.get('education', [])}")
            print(f"  Parse Quality: {result.get('parse_quality')}")


if __name__ == "__main__":
    main()
