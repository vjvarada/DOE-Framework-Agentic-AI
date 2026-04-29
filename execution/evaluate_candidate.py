#!/usr/bin/env python3
"""
Candidate Evaluator - Score and rank candidates against job requirements.

Reads parsed resume JSON and compares against job description requirements.
Outputs structured evaluation with scores and recommendations.

Usage:
    python evaluate_candidate.py --resume .tmp/parsed/candidate.json --jd .tmp/jds/role.json --output .tmp/evaluations/
    python evaluate_candidate.py --resumes-dir .tmp/parsed/ --jd .tmp/jds/role.json --output .tmp/evaluations/ --rank
    python evaluate_candidate.py --resume .tmp/parsed/candidate.json --jd .tmp/jds/role.json --copilot
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional


def normalize_skill(skill: str) -> str:
    """Normalize a skill name for comparison."""
    return skill.lower().strip().replace("-", " ").replace("_", " ").replace(".", "")


def compute_skill_match(candidate_skills: list, required_skills: list) -> dict:
    """Compute skill overlap between candidate and requirements."""
    if not required_skills:
        return {"score": 5, "matched": [], "missing": [], "extra": list(candidate_skills)}

    norm_candidate = {normalize_skill(s): s for s in candidate_skills}
    norm_required = {normalize_skill(s): s for s in required_skills}

    matched = []
    missing = []
    for norm_req, orig_req in norm_required.items():
        found = False
        for norm_cand, orig_cand in norm_candidate.items():
            if norm_req in norm_cand or norm_cand in norm_req:
                matched.append({"required": orig_req, "candidate_has": orig_cand})
                found = True
                break
        if not found:
            missing.append(orig_req)

    extra = [s for s in candidate_skills
             if not any(normalize_skill(s) in normalize_skill(r) or normalize_skill(r) in normalize_skill(s)
                        for r in required_skills)]

    if not required_skills:
        score = 5
    else:
        score = round((len(matched) / len(required_skills)) * 10, 1)

    return {
        "score": min(score, 10),
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "match_pct": round(len(matched) / max(len(required_skills), 1) * 100, 1)
    }


def compute_experience_match(candidate_years: Optional[float], required_range: str) -> dict:
    """Score experience against requirements."""
    if candidate_years is None:
        return {"score": 5, "note": "Experience years not detected in resume"}

    # Parse required range like "2-5 years" or "5+ years"
    import re
    match = re.search(r'(\d+)\s*[-–]\s*(\d+)', required_range)
    if match:
        min_years = int(match.group(1))
        max_years = int(match.group(2))
    else:
        match = re.search(r'(\d+)\+?', required_range)
        if match:
            min_years = int(match.group(1))
            max_years = min_years + 5
        else:
            return {"score": 5, "note": f"Could not parse requirement: {required_range}"}

    if candidate_years < min_years:
        deficit = min_years - candidate_years
        score = max(0, 7 - deficit * 2)
        note = f"Under-experienced: {candidate_years}y vs {min_years}-{max_years}y required"
    elif candidate_years > max_years + 3:
        score = 6
        note = f"Over-experienced: {candidate_years}y vs {min_years}-{max_years}y required (may be overqualified)"
    elif candidate_years > max_years:
        score = 8
        note = f"Exceeds range: {candidate_years}y vs {min_years}-{max_years}y required"
    else:
        score = 9
        note = f"Good fit: {candidate_years}y within {min_years}-{max_years}y required"

    return {"score": round(score, 1), "candidate_years": candidate_years,
            "required_range": required_range, "note": note}


def compute_education_match(candidate_education: list, required_education: str) -> dict:
    """Score education against requirements."""
    if not candidate_education:
        return {"score": 5, "note": "Education not detected in resume"}

    edu_text = " ".join(candidate_education).lower()
    score = 5
    notes = []

    if any(term in edu_text for term in ["ph.d", "phd", "doctor"]):
        score = 10
        notes.append("PhD holder")
    elif any(term in edu_text for term in ["m.tech", "mtech", "m.e", "m.sc", "master", "mba"]):
        score = 9
        notes.append("Master's degree")
    elif any(term in edu_text for term in ["b.tech", "btech", "b.e", "b.sc", "bachelor"]):
        score = 7
        notes.append("Bachelor's degree")
    elif any(term in edu_text for term in ["diploma"]):
        score = 5
        notes.append("Diploma")

    # Bonus for relevant fields
    relevant_fields = ["mechanical", "electrical", "electronics", "computer", "software",
                       "materials", "manufacturing", "robotics", "mechatronics", "embedded"]
    if any(field in edu_text for field in relevant_fields):
        score = min(score + 1, 10)
        notes.append("Relevant field of study")

    return {"score": score, "education": candidate_education, "note": "; ".join(notes)}


def compute_industry_bonus(raw_text: str) -> dict:
    """Bonus points for 3D printing / manufacturing industry experience."""
    if not raw_text:
        return {"score": 0, "signals": []}

    text_lower = raw_text.lower()
    industry_signals = []

    keywords = {
        "3d printing": 2, "additive manufacturing": 2, "3d printer": 2,
        "fdm": 1.5, "sls": 1.5, "sla": 1, "cnc": 1,
        "cad": 1, "solidworks": 1, "catia": 1, "fusion 360": 1,
        "manufacturing": 0.5, "prototyping": 1, "rapid prototyping": 1.5,
        "digital fabrication": 2, "gcode": 1.5, "slicing": 1.5,
        "fea": 0.5, "cfd": 0.5, "dfm": 1, "dfa": 1,
        "firmware": 0.5, "embedded": 0.5, "pcb": 0.5, "motor control": 1,
        "polymer": 1, "filament": 1.5, "nylon": 0.5, "pla": 0.5, "abs": 0.5,
        "robotics": 0.5, "automation": 0.5, "iot": 0.5,
        "startup": 0.5, "product development": 0.5
    }

    total_bonus = 0
    for keyword, weight in keywords.items():
        if keyword in text_lower:
            industry_signals.append(keyword)
            total_bonus += weight

    return {
        "score": min(round(total_bonus, 1), 5),
        "signals": industry_signals
    }


def evaluate_candidate(resume_data: dict, jd_data: dict) -> dict:
    """
    Evaluate a candidate against a job description.

    Returns evaluation with scores and recommendation.
    """
    skills_eval = compute_skill_match(
        resume_data.get("skills", []),
        jd_data.get("required_skills", [])
    )
    exp_eval = compute_experience_match(
        resume_data.get("experience_years"),
        jd_data.get("experience_required", "")
    )
    edu_eval = compute_education_match(
        resume_data.get("education", []),
        jd_data.get("education_required", "")
    )
    industry_eval = compute_industry_bonus(resume_data.get("raw_text", ""))

    # Weighted overall score
    weights = {"skills": 0.35, "experience": 0.25, "education": 0.15, "industry": 0.25}
    overall = (
        skills_eval["score"] * weights["skills"] +
        exp_eval["score"] * weights["experience"] +
        edu_eval["score"] * weights["education"] +
        industry_eval["score"] * weights["industry"]
    )
    overall = round(overall, 1)

    # Recommendation
    if overall >= 8:
        recommendation = "Strong Hire"
    elif overall >= 6.5:
        recommendation = "Hire"
    elif overall >= 5:
        recommendation = "Maybe"
    else:
        recommendation = "No Hire"

    return {
        "candidate": {
            "name": resume_data.get("name"),
            "email": resume_data.get("email"),
            "file": resume_data.get("file"),
        },
        "role": {
            "title": jd_data.get("title"),
            "department": jd_data.get("department"),
            "level": jd_data.get("level"),
        },
        "scores": {
            "skills": skills_eval,
            "experience": exp_eval,
            "education": edu_eval,
            "industry_fit": industry_eval,
            "overall": overall,
            "weights": weights
        },
        "recommendation": recommendation,
        "evaluated_at": datetime.now().isoformat()
    }


def format_evaluation_text(evaluation: dict) -> str:
    """Format evaluation as readable text."""
    e = evaluation
    c = e["candidate"]
    r = e["role"]
    s = e["scores"]

    text = f"{'='*60}\n"
    text += f"CANDIDATE EVALUATION REPORT\n"
    text += f"{'='*60}\n\n"
    text += f"Candidate:  {c.get('name', 'N/A')}\n"
    text += f"Email:      {c.get('email', 'N/A')}\n"
    text += f"Resume:     {c.get('file', 'N/A')}\n\n"
    text += f"Position:   {r.get('title', 'N/A')}\n"
    text += f"Department: {r.get('department', 'N/A')}\n"
    text += f"Level:      {r.get('level', 'N/A')}\n\n"

    text += f"--- SCORES ---\n"
    text += f"  Skills Match:    {s['skills']['score']}/10 ({s['skills'].get('match_pct', 'N/A')}% overlap)\n"
    text += f"  Experience:      {s['experience']['score']}/10 — {s['experience'].get('note', '')}\n"
    text += f"  Education:       {s['education']['score']}/10 — {s['education'].get('note', '')}\n"
    text += f"  Industry Fit:    {s['industry_fit']['score']}/5 — {len(s['industry_fit'].get('signals', []))} signals\n"
    text += f"\n  OVERALL:         {s['overall']}/10\n"
    text += f"  RECOMMENDATION:  {e['recommendation']}\n\n"

    if s['skills'].get('matched'):
        text += f"  Skills Matched: {', '.join(m['required'] for m in s['skills']['matched'])}\n"
    if s['skills'].get('missing'):
        text += f"  Skills Missing: {', '.join(s['skills']['missing'])}\n"
    if s['industry_fit'].get('signals'):
        text += f"  Industry Signals: {', '.join(s['industry_fit']['signals'][:10])}\n"

    text += f"\n{'='*60}\n"
    return text


def main():
    parser = argparse.ArgumentParser(description="Evaluate candidates against job descriptions")
    parser.add_argument("--resume", help="Path to parsed resume JSON")
    parser.add_argument("--resumes-dir", help="Directory of parsed resume JSONs (for batch ranking)")
    parser.add_argument("--jd", required=True, help="Path to job description JSON")
    parser.add_argument("--output", default=".tmp/evaluations/", help="Output directory")
    parser.add_argument("--rank", action="store_true", help="Rank all candidates and output leaderboard")
    parser.add_argument("--copilot", action="store_true",
                        help="Output structured prompt for Copilot deep analysis")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load JD
    with open(args.jd, "r", encoding="utf-8") as f:
        jd_data = json.load(f)
    print(f"Job: {jd_data.get('title')} ({jd_data.get('department')})")

    if args.resumes_dir or args.rank:
        resumes_path = Path(args.resumes_dir or args.resume).parent if args.resume else Path(args.resumes_dir)
        resume_files = sorted(resumes_path.glob("*.json"))
        resume_files = [f for f in resume_files if not f.name.startswith("_")]

        if not resume_files:
            print(f"No resume JSONs found in {resumes_path}")
            sys.exit(1)

        print(f"Evaluating {len(resume_files)} candidate(s)...\n")
        evaluations = []

        for rf in resume_files:
            with open(rf, "r", encoding="utf-8") as f:
                resume_data = json.load(f)
            if resume_data.get("parse_quality") == "failed":
                print(f"  Skipping {rf.name} (parse failed)")
                continue
            evaluation = evaluate_candidate(resume_data, jd_data)
            evaluations.append(evaluation)

            out_file = output_dir / f"eval_{rf.stem}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(evaluation, f, indent=2, ensure_ascii=False)

            print(format_evaluation_text(evaluation))

        # Rank and save leaderboard
        evaluations.sort(key=lambda e: e["scores"]["overall"], reverse=True)
        leaderboard = {
            "role": jd_data.get("title"),
            "total_candidates": len(evaluations),
            "rankings": [
                {
                    "rank": i + 1,
                    "name": e["candidate"].get("name"),
                    "email": e["candidate"].get("email"),
                    "overall_score": e["scores"]["overall"],
                    "recommendation": e["recommendation"]
                }
                for i, e in enumerate(evaluations)
            ],
            "evaluated_at": datetime.now().isoformat()
        }
        lb_file = output_dir / "_leaderboard.json"
        with open(lb_file, "w", encoding="utf-8") as f:
            json.dump(leaderboard, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*60}")
        print(f"LEADERBOARD — {jd_data.get('title')}")
        print(f"{'='*60}")
        for r in leaderboard["rankings"]:
            print(f"  #{r['rank']}  {r['overall_score']:>5.1f}/10  {r['recommendation']:<12}  {r.get('name', 'N/A')}")
        print(f"\nSaved to {lb_file}")

    else:
        if not args.resume:
            print("ERROR: --resume or --resumes-dir required")
            sys.exit(1)

        with open(args.resume, "r", encoding="utf-8") as f:
            resume_data = json.load(f)

        evaluation = evaluate_candidate(resume_data, jd_data)

        if args.copilot:
            print("\n--- COPILOT EVALUATION PROMPT ---")
            print(f"Perform a detailed evaluation of this candidate for the role of {jd_data.get('title')} at Fracktal Works.\n")
            print(f"JD Requirements:\n{json.dumps({k: v for k, v in jd_data.items() if k != 'company_description'}, indent=2)}\n")
            resume_summary = {k: v for k, v in resume_data.items() if k != "raw_text"}
            print(f"Parsed Resume:\n{json.dumps(resume_summary, indent=2)}\n")
            print(f"Automated Scores:\n{json.dumps(evaluation['scores'], indent=2)}\n")
            print("Please provide: strengths, weaknesses, concerns, interview questions to ask, and final recommendation.")
            print("--- END PROMPT ---")
        else:
            out_file = output_dir / f"eval_{Path(args.resume).stem}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(evaluation, f, indent=2, ensure_ascii=False)
            print(format_evaluation_text(evaluation))
            print(f"Saved to {out_file}")


if __name__ == "__main__":
    main()
