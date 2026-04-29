#!/usr/bin/env python3
"""
Job Description Generator for Fracktal Works.

Generates structured job descriptions tailored to Fracktal Works' 3D printing
and digital manufacturing context. In Copilot mode, outputs a prompt for
Copilot to write the actual content.

Usage:
    python generate_job_description.py --title "Mechanical Design Engineer" --department "Engineering" --level "mid" --output ".tmp/jds/"
    python generate_job_description.py --title "Embedded Systems Engineer" --department "R&D" --level "senior" --copilot
    python generate_job_description.py --from-file ".tmp/jd_input.json" --output ".tmp/jds/"
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

COMPANY_BOILERPLATE = """Fracktal Works is a pioneering 3D printing and digital manufacturing company founded in 2013. We design and manufacture industrial-grade 3D printers (Julia, Dragon, Twin Dragon, Snowflake, Volterra, Apollo SLS), develop proprietary slicing software (Fracktory), and provide comprehensive 3D printing services across FDM, SLS, HP MJF, SLA, and Vacuum Casting technologies. Our mission is to empower sustainable development through digital fabrication, making high-quality affordable manufacturing accessible to every individual and organization. Based in Bangalore, India, we serve clients across automotive, healthcare, aerospace, manufacturing, jewelry, dental, and entertainment industries."""

DEPARTMENTS = {
    "engineering": {
        "context": "3D printer design, mechanical systems, CAD/CAM, FEA, DFM",
        "typical_skills": ["SolidWorks", "CATIA", "Fusion 360", "FEA", "GD&T", "DFM", "Sheet Metal", "3D Printing"]
    },
    "r&d": {
        "context": "New product development, materials research, print process optimization",
        "typical_skills": ["Research methodology", "Prototyping", "Data analysis", "Technical writing", "Patent drafting"]
    },
    "embedded": {
        "context": "Firmware, PCB design, motor control, sensors, IoT connectivity",
        "typical_skills": ["C/C++", "ARM Cortex", "STM32", "RTOS", "PCB Design", "KiCad/Altium", "UART/SPI/I2C", "Motor Control"]
    },
    "software": {
        "context": "Slicer software (Fracktory), cloud platform, IoT dashboard, internal tools",
        "typical_skills": ["Python", "C++", "JavaScript", "React", "Qt", "3D Graphics", "OpenGL", "REST API", "Docker"]
    },
    "materials": {
        "context": "Polymer science, filament testing, print parameter optimization, material qualification",
        "typical_skills": ["Polymer Chemistry", "Material Testing", "DSC/TGA", "Tensile Testing", "Print Optimization"]
    },
    "service": {
        "context": "3D printer installation, calibration, maintenance, customer training",
        "typical_skills": ["Troubleshooting", "Electromechanical Systems", "Customer Training", "Technical Documentation"]
    },
    "sales": {
        "context": "B2B sales in manufacturing sector, solution selling, account management",
        "typical_skills": ["B2B Sales", "CRM", "Technical Presentations", "Account Management", "Manufacturing Knowledge"]
    },
    "production": {
        "context": "3D printer assembly, quality control, production planning, supply chain",
        "typical_skills": ["Assembly", "Quality Control", "Lean Manufacturing", "Inventory Management", "ERP"]
    },
    "marketing": {
        "context": "Technical content, social media, events, brand management for B2B tech company",
        "typical_skills": ["Content Marketing", "SEO", "Social Media", "Technical Writing", "Graphic Design", "Video Production"]
    },
    "qa": {
        "context": "Product quality assurance, testing protocols, standards compliance",
        "typical_skills": ["Quality Management", "ISO 9001", "Testing Protocols", "Statistical Analysis", "Root Cause Analysis"]
    }
}

LEVEL_SPECS = {
    "intern": {"experience": "0 years (current student or recent graduate)", "education": "Pursuing or recently completed B.Tech/B.E/equivalent"},
    "junior": {"experience": "0-2 years", "education": "B.Tech/B.E or equivalent"},
    "mid": {"experience": "2-5 years", "education": "B.Tech/B.E or equivalent; M.Tech preferred"},
    "senior": {"experience": "5-10 years", "education": "B.Tech/B.E or equivalent; M.Tech preferred"},
    "lead": {"experience": "8-15 years", "education": "B.Tech/B.E or M.Tech; MBA a plus for management roles"},
    "head": {"experience": "12+ years", "education": "B.Tech/B.E or M.Tech; MBA preferred for leadership"}
}


def generate_jd_structure(title: str, department: str, level: str,
                          responsibilities: list = None, skills: list = None,
                          location: str = "Bangalore, India",
                          work_type: str = "On-site") -> dict:
    """Generate a structured job description."""
    dept_key = department.lower().replace(" ", "").replace("&", "and")
    dept_info = DEPARTMENTS.get(dept_key, {"context": department, "typical_skills": []})
    level_info = LEVEL_SPECS.get(level.lower(), LEVEL_SPECS["mid"])

    jd = {
        "company": "Fracktal Works Pvt. Ltd",
        "title": title,
        "department": department,
        "level": level.capitalize(),
        "location": location,
        "work_type": work_type,
        "company_description": COMPANY_BOILERPLATE,
        "department_context": dept_info["context"],
        "experience_required": level_info["experience"],
        "education_required": level_info["education"],
        "responsibilities": responsibilities or [],
        "required_skills": skills or dept_info.get("typical_skills", []),
        "preferred_skills": [],
        "benefits": [
            "Work with cutting-edge 3D printing and digital manufacturing technology",
            "Fast-paced startup environment with direct impact on products",
            "Hands-on experience with hardware and software development",
            "Collaborative and innovation-driven culture",
            "Learning and growth opportunities in a rapidly evolving industry"
        ],
        "generated_at": datetime.now().isoformat(),
        "status": "draft"
    }
    return jd


def format_jd_markdown(jd: dict) -> str:
    """Format JD struct as a readable Markdown document."""
    md = f"# {jd['title']}\n\n"
    md += f"**Company:** {jd['company']}  \n"
    md += f"**Department:** {jd['department']}  \n"
    md += f"**Level:** {jd['level']}  \n"
    md += f"**Location:** {jd['location']}  \n"
    md += f"**Work Type:** {jd['work_type']}  \n\n"

    md += "## About Fracktal Works\n\n"
    md += jd['company_description'] + "\n\n"

    md += "## Role Summary\n\n"
    md += f"We are looking for a {jd['level']}-level {jd['title']} to join our {jd['department']} team. "
    md += f"This role involves {jd['department_context']}.\n\n"

    md += f"**Experience:** {jd['experience_required']}  \n"
    md += f"**Education:** {jd['education_required']}\n\n"

    if jd['responsibilities']:
        md += "## Key Responsibilities\n\n"
        for r in jd['responsibilities']:
            md += f"- {r}\n"
        md += "\n"

    if jd['required_skills']:
        md += "## Required Skills\n\n"
        for s in jd['required_skills']:
            md += f"- {s}\n"
        md += "\n"

    if jd['preferred_skills']:
        md += "## Preferred Skills\n\n"
        for s in jd['preferred_skills']:
            md += f"- {s}\n"
        md += "\n"

    md += "## What We Offer\n\n"
    for b in jd['benefits']:
        md += f"- {b}\n"
    md += "\n"

    md += "## How to Apply\n\n"
    md += "Send your resume and a brief cover letter to careers@fracktal.in with the subject line: "
    md += f'"{jd["title"]} Application - [Your Name]"\n\n'

    md += "---\n"
    md += f"*Fracktal Works is an equal opportunity employer. Generated on {jd['generated_at'][:10]}*\n"

    return md


def main():
    parser = argparse.ArgumentParser(description="Generate job descriptions for Fracktal Works")
    parser.add_argument("--title", help="Job title")
    parser.add_argument("--department", help="Department name")
    parser.add_argument("--level", default="mid",
                        choices=["intern", "junior", "mid", "senior", "lead", "head"],
                        help="Seniority level")
    parser.add_argument("--location", default="Bangalore, India", help="Job location")
    parser.add_argument("--work-type", default="On-site",
                        choices=["On-site", "Remote", "Hybrid"], help="Work arrangement")
    parser.add_argument("--responsibilities", nargs="+", help="Key responsibilities")
    parser.add_argument("--skills", nargs="+", help="Required skills")
    parser.add_argument("--from-file", help="Load input from JSON file")
    parser.add_argument("--output", default=".tmp/jds/", help="Output directory")
    parser.add_argument("--copilot", action="store_true",
                        help="Output prompt for Copilot to generate full JD content")
    args = parser.parse_args()

    if args.from_file:
        with open(args.from_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        title = data.get("title", args.title)
        department = data.get("department", args.department)
        level = data.get("level", args.level or "mid")
        responsibilities = data.get("responsibilities", args.responsibilities)
        skills = data.get("skills", args.skills)
        location = data.get("location", args.location)
        work_type = data.get("work_type", args.work_type)
    else:
        title = args.title
        department = args.department
        level = args.level
        responsibilities = args.responsibilities
        skills = args.skills
        location = args.location
        work_type = args.work_type

    if not title or not department:
        print("ERROR: --title and --department are required (or use --from-file)")
        sys.exit(1)

    jd = generate_jd_structure(title, department, level, responsibilities, skills, location, work_type)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    slug = title.lower().replace(" ", "-")
    json_file = output_dir / f"{slug}.json"
    md_file = output_dir / f"{slug}.md"

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(jd, f, indent=2, ensure_ascii=False)
    print(f"  Saved JD structure: {json_file}")

    if args.copilot:
        print("\n--- COPILOT JD GENERATION PROMPT ---")
        print(f"Generate a complete, professional job description for the following role at Fracktal Works:")
        print(f"\nRole: {title}")
        print(f"Department: {department} ({jd['department_context']})")
        print(f"Level: {level.capitalize()} ({jd['experience_required']})")
        print(f"Location: {location} ({work_type})")
        print(f"\nCompany context: {COMPANY_BOILERPLATE[:200]}...")
        if responsibilities:
            print(f"\nUser-specified responsibilities: {responsibilities}")
        if skills:
            print(f"User-specified skills: {skills}")
        print(f"\nDefault department skills: {jd['required_skills']}")
        print(f"\nPlease write a compelling, detailed JD with: Role Summary, Key Responsibilities (8-10),")
        print(f"Required Qualifications, Preferred Qualifications, Technical Skills, Soft Skills,")
        print(f"What We Offer, and Application Instructions.")
        print("--- END PROMPT ---")
    else:
        md_content = format_jd_markdown(jd)
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"  Saved JD markdown: {md_file}")
        print(f"\n  Preview:\n")
        # Print first 20 lines
        for line in md_content.split('\n')[:20]:
            print(f"    {line}")
        print("    ...")


if __name__ == "__main__":
    main()
