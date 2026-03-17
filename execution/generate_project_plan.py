#!/usr/bin/env python3
"""
Technical Project Plan Generator

Generates work breakdown structures, Gantt charts (Mermaid), risk registers,
and compiles full project plans from research and requirements data.

Usage:
    python generate_project_plan.py --mode wbs --project-name "Drone Inspection" --output "outputs/drone/wbs.md"
    python generate_project_plan.py --mode gantt --project-name "Drone Inspection" --wbs "outputs/drone/wbs.md" --start-date 2025-06-01 --output "outputs/drone/gantt_chart.md"
    python generate_project_plan.py --mode risks --project-name "Drone Inspection" --domain "autonomous drones" --output "outputs/drone/risk_register.md"
    python generate_project_plan.py --mode references --research-dir ".tmp/drone/" --output "outputs/drone/references.md"
    python generate_project_plan.py --mode compile --project-name "Drone Inspection" --project-dir "outputs/drone/" --output "outputs/drone/project_plan.md"
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


#  Helpers 


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_json_safe(path: Path) -> dict | list:
    """Load JSON, return empty dict on failure."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def write_md(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {path}")


def today_str() -> str:
    return datetime.now().strftime("%B %d, %Y")


#  WBS Generator 


def generate_wbs(project_name: str, requirements_file: str | None, output: str) -> None:
    """
    Generate a Work Breakdown Structure template for a systems engineering project.
    If a requirements JSON is supplied, incorporates requirement categories.
    """
    print(f"Generating WBS for: {project_name}")

    reqs = {}
    if requirements_file and Path(requirements_file).exists():
        reqs = load_json_safe(Path(requirements_file))

    md = []
    md.append(f"# Work Breakdown Structure — {project_name}")
    md.append(f"\n*Generated: {today_str()}*\n")
    md.append("---\n")

    # Standard V-model phases for HW/SW systems engineering
    phases = [
        {
            "id": "1",
            "name": "Concept & Requirements",
            "packages": [
                ("1.1", "Stakeholder Needs Analysis", "Gather and document stakeholder needs", "1-2 weeks"),
                ("1.2", "Requirements Specification", "Create SRS / system requirements", "2-3 weeks"),
                ("1.3", "Feasibility Study & Trade Studies", "Evaluate technical feasibility of approaches", "1-2 weeks"),
                ("1.4", "Concept of Operations (ConOps)", "Define operational scenarios", "1 week"),
            ],
        },
        {
            "id": "2",
            "name": "System Architecture & Design",
            "packages": [
                ("2.1", "System Architecture Design", "High-level block diagrams, interface definitions", "2-3 weeks"),
                ("2.2", "Hardware-Software Partitioning", "Allocate functions to HW vs SW", "1-2 weeks"),
                ("2.3", "Interface Control Documents (ICDs)", "Define all inter-subsystem interfaces", "1-2 weeks"),
                ("2.4", "Technology Selection & BoM", "Select components, create Bill of Materials", "1-2 weeks"),
                ("2.5", "System Design Review (SDR)", "Formal design review milestone", "1 week"),
            ],
        },
        {
            "id": "3",
            "name": "Hardware Development",
            "packages": [
                ("3.1", "Schematic Design", "Circuit design for all PCBs / subsystems", "3-4 weeks"),
                ("3.2", "PCB Layout & Fabrication", "Layout, DFM review, order PCBs", "2-4 weeks"),
                ("3.3", "Mechanical Design & CAD", "Enclosures, mounts, thermal design", "3-4 weeks"),
                ("3.4", "Hardware Prototype Build", "Assemble first prototypes", "2-3 weeks"),
                ("3.5", "Hardware Unit Testing", "Test individual HW modules", "2-3 weeks"),
            ],
        },
        {
            "id": "4",
            "name": "Software Development",
            "packages": [
                ("4.1", "Software Architecture", "Module decomposition, data-flow, OS selection", "1-2 weeks"),
                ("4.2", "Firmware / Embedded SW", "Low-level drivers, RTOS tasks, BSP", "4-6 weeks"),
                ("4.3", "Application Software", "High-level logic, algorithms, UI/UX", "4-6 weeks"),
                ("4.4", "Communication / Middleware", "Protocols, APIs, cloud connectivity", "2-3 weeks"),
                ("4.5", "Software Unit Testing", "Unit tests, static analysis, code review", "2-3 weeks"),
            ],
        },
        {
            "id": "5",
            "name": "Integration & Test",
            "packages": [
                ("5.1", "HW-SW Integration", "Bring-up firmware on target hardware", "2-3 weeks"),
                ("5.2", "Subsystem Integration Testing", "Test composed subsystems end-to-end", "2-3 weeks"),
                ("5.3", "System Integration Testing", "Full system functional testing", "2-3 weeks"),
                ("5.4", "Environmental & Stress Testing", "Thermal, vibration, EMC (if applicable)", "1-3 weeks"),
                ("5.5", "Test Readiness Review (TRR)", "Formal milestone before V&V", "1 week"),
            ],
        },
        {
            "id": "6",
            "name": "Verification & Validation",
            "packages": [
                ("6.1", "Requirements Verification", "Verify each requirement is met (test, analysis, inspection)", "2-3 weeks"),
                ("6.2", "Validation in Operational Environment", "Validate system performs in real conditions", "2-3 weeks"),
                ("6.3", "Regulatory / Compliance Testing", "Standards compliance testing (if applicable)", "1-3 weeks"),
                ("6.4", "User Acceptance Testing (UAT)", "End-user validation sessions", "1-2 weeks"),
            ],
        },
        {
            "id": "7",
            "name": "Production & Deployment",
            "packages": [
                ("7.1", "Production Planning", "DFM, test fixtures, supply chain", "2-3 weeks"),
                ("7.2", "Pilot Production Run", "Small batch production validation", "2-3 weeks"),
                ("7.3", "Deployment & Installation", "Field deployment, commissioning", "1-3 weeks"),
                ("7.4", "Training & Documentation", "User manuals, training sessions", "1-2 weeks"),
            ],
        },
        {
            "id": "8",
            "name": "Operations & Maintenance",
            "packages": [
                ("8.1", "Monitoring & Support", "Operational monitoring, helpdesk", "Ongoing"),
                ("8.2", "Maintenance & Updates", "Bug fixes, firmware updates, HW repairs", "Ongoing"),
                ("8.3", "Lessons Learned & Retrospective", "Post-project review", "1 week"),
            ],
        },
    ]

    # Render WBS table
    md.append("## WBS Overview\n")
    md.append("| WBS ID | Work Package | Description | Est. Duration |")
    md.append("|--------|-------------|-------------|---------------|")

    for phase in phases:
        md.append(f"| **{phase['id']}** | **{phase['name']}** | | |")
        for pkg in phase["packages"]:
            md.append(f"| {pkg[0]} | {pkg[1]} | {pkg[2]} | {pkg[3]} |")

    md.append("")

    # Render WBS tree (indented list)
    md.append("## WBS Tree\n")
    md.append(f"- **{project_name}**")
    for phase in phases:
        md.append(f"  - **{phase['id']} {phase['name']}**")
        for pkg in phase["packages"]:
            md.append(f"    - {pkg[0]} {pkg[1]} ({pkg[3]})")
    md.append("")

    # Dependencies note
    md.append("## Key Dependencies\n")
    md.append("| Predecessor | Successor | Type | Notes |")
    md.append("|-------------|-----------|------|-------|")
    md.append("| 1.2 Requirements Specification | 2.1 System Architecture Design | FS | Requirements must be baselined |")
    md.append("| 2.1 System Architecture Design | 3.1 Schematic Design | FS | Architecture drives HW design |")
    md.append("| 2.1 System Architecture Design | 4.1 Software Architecture | FS | Architecture drives SW design |")
    md.append("| 2.4 Technology Selection | 3.2 PCB Layout & Fabrication | FS | Components must be selected |")
    md.append("| 3.4 HW Prototype Build | 5.1 HW-SW Integration | FS | Need hardware to integrate |")
    md.append("| 4.2 Firmware / Embedded SW | 5.1 HW-SW Integration | FS | Need firmware to integrate |")
    md.append("| 5.3 System Integration Testing | 6.1 Requirements Verification | FS | System must be integrated |")
    md.append("| 6.4 User Acceptance Testing | 7.1 Production Planning | FS | Must pass UAT |")
    md.append("")

    md.append("## Notes\n")
    md.append("- Durations are initial PERT-style estimates — refine with team input")
    md.append("- Phases 3 and 4 (HW & SW) typically run in parallel")
    md.append("- Budget ~20-30% of total timeline for Integration & Test")
    md.append("- Include phase gate reviews between major phases (SDR, PDR, CDR, TRR)")
    md.append("- Customize work packages based on your specific project requirements")
    md.append("")

    md.append("<!-- COPILOT: Customize this WBS based on the specific project requirements. -->")
    md.append("<!-- Add, remove, or modify work packages as needed. Update duration estimates -->")
    md.append("<!-- based on team capacity and project constraints. -->")

    write_md(Path(output), "\n".join(md))


#  Gantt Chart Generator 


def _parse_duration(dur_str: str) -> int:
    """Convert '2-3 weeks' -> midpoint in days."""
    m = re.search(r"(\d+)\s*-\s*(\d+)\s*week", dur_str, re.IGNORECASE)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        return int((lo + hi) / 2 * 7)
    m = re.search(r"(\d+)\s*week", dur_str, re.IGNORECASE)
    if m:
        return int(m.group(1)) * 7
    m = re.search(r"(\d+)\s*day", dur_str, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return 14  # default 2 weeks


def generate_gantt(project_name: str, wbs_file: str | None, start_date: str, output: str) -> None:
    """Generate a Mermaid Gantt chart from WBS data."""
    print(f"Generating Gantt chart for: {project_name}")

    start = datetime.strptime(start_date, "%Y-%m-%d")

    # Parse WBS if provided (read the markdown table)
    tasks = []
    if wbs_file and Path(wbs_file).exists():
        with open(wbs_file, "r", encoding="utf-8") as f:
            content = f.read()
        # Parse table rows — only from WBS Overview section, match numeric IDs like 1.1, 2.3
        in_wbs_table = False
        for line in content.split("\n"):
            line = line.strip()
            if "WBS Overview" in line or "WBS ID" in line:
                in_wbs_table = True
                continue
            if in_wbs_table and line.startswith("##") and "WBS Overview" not in line:
                in_wbs_table = False  # moved to a different section
                continue
            if not in_wbs_table or not line.startswith("|") or "---" in line or "WBS ID" in line:
                continue
            cells = [c.strip().strip("*") for c in line.split("|") if c.strip()]
            # Only match rows where first cell is a numeric WBS ID (e.g. 1.1, 3.4)
            if len(cells) >= 4 and cells[0] and re.match(r'^\d+\.\d+$', cells[0]):
                tasks.append({
                    "id": cells[0].strip("*").strip(),
                    "name": cells[1].strip("*").strip(),
                    "desc": cells[2] if len(cells) > 2 else "",
                    "duration": cells[3] if len(cells) > 3 else "2 weeks",
                })

    # Default tasks if WBS not parsed
    if not tasks:
        tasks = [
            {"id": "1.1", "name": "Stakeholder Analysis", "duration": "1-2 weeks"},
            {"id": "1.2", "name": "Requirements Specification", "duration": "2-3 weeks"},
            {"id": "2.1", "name": "System Architecture Design", "duration": "2-3 weeks"},
            {"id": "2.2", "name": "HW-SW Partitioning", "duration": "1-2 weeks"},
            {"id": "3.1", "name": "Schematic Design", "duration": "3-4 weeks"},
            {"id": "3.2", "name": "PCB Layout & Fab", "duration": "2-4 weeks"},
            {"id": "4.1", "name": "Software Architecture", "duration": "1-2 weeks"},
            {"id": "4.2", "name": "Firmware Development", "duration": "4-6 weeks"},
            {"id": "4.3", "name": "Application Software", "duration": "4-6 weeks"},
            {"id": "5.1", "name": "HW-SW Integration", "duration": "2-3 weeks"},
            {"id": "5.3", "name": "System Integration Test", "duration": "2-3 weeks"},
            {"id": "6.1", "name": "Requirements Verification", "duration": "2-3 weeks"},
            {"id": "7.1", "name": "Production Planning", "duration": "2-3 weeks"},
            {"id": "7.3", "name": "Deployment", "duration": "1-3 weeks"},
        ]

    md = []
    md.append(f"# Project Schedule — {project_name}")
    md.append(f"\n*Generated: {today_str()}*")
    md.append(f"*Project Start: {start.strftime('%B %d, %Y')}*\n")
    md.append("---\n")

    # Build Mermaid Gantt
    md.append("## Gantt Chart\n")
    md.append("`mermaid")
    md.append("gantt")
    md.append(f"    title {project_name} — Project Schedule")
    md.append("    dateFormat  YYYY-MM-DD")
    md.append("    axisFormat  %b %Y")
    md.append("")

    # Group tasks by phase
    phase_map = defaultdict(list)
    for t in tasks:
        phase_num = t["id"].split(".")[0]
        phase_map[phase_num].append(t)

    phase_names = {
        "1": "Concept & Requirements",
        "2": "System Architecture & Design",
        "3": "Hardware Development",
        "4": "Software Development",
        "5": "Integration & Test",
        "6": "Verification & Validation",
        "7": "Production & Deployment",
        "8": "Operations & Maintenance",
    }

    running_date = start
    task_dates = {}  # id -> (start, end)

    for phase_num in sorted(phase_map.keys()):
        pname = phase_names.get(phase_num, f"Phase {phase_num}")
        md.append(f"    section {pname}")

        # HW (3) and SW (4) run in parallel
        if phase_num == "4" and "3" in task_dates:
            # Rewind to start of phase 3
            phase3_start = min(s for s, e in [task_dates[t["id"]] for t in phase_map.get("3", []) if t["id"] in task_dates])
            running_date = phase3_start

        for t in phase_map[phase_num]:
            days = _parse_duration(t["duration"])
            task_end = running_date + timedelta(days=days)

            safe_id = "t" + t["id"].replace(".", "_")
            md.append(f"    {t['name']}  :{safe_id}, {running_date.strftime('%Y-%m-%d')}, {days}d")

            task_dates[t["id"]] = (running_date, task_end)
            running_date = task_end

    md.append("`\n")

    # Milestone table
    md.append("## Milestones\n")
    md.append("| Milestone | Target Date | Dependencies | Status |")
    md.append("|-----------|------------|--------------|--------|")

    milestones = [
        ("Requirements Baseline", "1.2", "Requirements Specification complete"),
        ("System Design Review (SDR)", "2.5" if any(t["id"] == "2.5" for t in tasks) else "2.1", "Architecture approved"),
        ("HW Prototype Ready", "3.4" if any(t["id"] == "3.4" for t in tasks) else "3.2", "First hardware available"),
        ("SW Alpha Release", "4.3" if any(t["id"] == "4.3" for t in tasks) else "4.2", "Core software functional"),
        ("Integration Complete", "5.3" if any(t["id"] == "5.3" for t in tasks) else "5.1", "System integrated"),
        ("Verification Complete", "6.1", "All requirements verified"),
        ("Production Release", "7.3" if any(t["id"] == "7.3" for t in tasks) else "7.1", "Ready for deployment"),
    ]

    for ms_name, dep_id, dep_desc in milestones:
        if dep_id in task_dates:
            _, end = task_dates[dep_id]
            md.append(f"| {ms_name} | {end.strftime('%Y-%m-%d')} | {dep_desc} | Planned |")
        else:
            md.append(f"| {ms_name} | TBD | {dep_desc} | Planned |")

    md.append("")

    # Timeline summary
    if task_dates:
        earliest = min(s for s, e in task_dates.values())
        latest = max(e for s, e in task_dates.values())
        total_days = (latest - earliest).days
        total_weeks = round(total_days / 7, 1)
        md.append(f"## Timeline Summary\n")
        md.append(f"- **Start Date:** {earliest.strftime('%Y-%m-%d')}")
        md.append(f"- **End Date:** {latest.strftime('%Y-%m-%d')}")
        md.append(f"- **Total Duration:** {total_days} days (~{total_weeks} weeks)")
        md.append("")

    md.append("## Critical Path Notes\n")
    md.append("- Hardware (Phase 3) and Software (Phase 4) run **in parallel**")
    md.append("- Integration (Phase 5) is the convergence point — delays in either HW or SW cascade here")
    md.append("- Budget buffer time before major milestones (typically 1-2 weeks)")
    md.append("- External dependencies (component procurement, regulatory review) are not shown — add these")
    md.append("")
    md.append("<!-- COPILOT: Customize task durations, dependencies, and milestones based on -->")
    md.append("<!-- the specific project requirements and team capacity. Add resource assignments. -->")

    write_md(Path(output), "\n".join(md))


#  Risk Register Generator 


def generate_risks(project_name: str, domain: str, output: str) -> None:
    """Generate a risk register template for a systems engineering project."""
    print(f"Generating risk register for: {project_name} (domain: {domain})")

    md = []
    md.append(f"# Risk Register — {project_name}")
    md.append(f"\n*Generated: {today_str()}*")
    md.append(f"*Domain: {domain}*\n")
    md.append("---\n")

    md.append("## Risk Matrix\n")
    md.append("| | **Low Impact (1)** | **Medium Impact (2)** | **High Impact (3)** | **Critical Impact (4)** |")
    md.append("|---|---|---|---|---|")
    md.append("| **High Probability (3)** | 3 — Medium | 6 — High | 9 — Critical | 12 — Critical |")
    md.append("| **Medium Probability (2)** | 2 — Low | 4 — Medium | 6 — High | 8 — High |")
    md.append("| **Low Probability (1)** | 1 — Low | 2 — Low | 3 — Medium | 4 — Medium |")
    md.append("")

    # Standard systems engineering risks
    risk_categories = {
        "Technical Risks": [
            ("T1", "Technology Maturity", "Selected technology/components may not be mature enough", 2, 3, "Mitigate", "Conduct early prototyping and proof-of-concept; have fallback technology identified"),
            ("T2", "Integration Complexity", "HW-SW integration more complex than anticipated", 3, 3, "Mitigate", "Plan dedicated integration sprints; create integration test plan early; use hardware-in-the-loop simulation"),
            ("T3", "Performance Shortfall", "System fails to meet performance requirements", 2, 3, "Mitigate", "Define performance budgets early; conduct incremental performance testing; have optimization plan"),
            ("T4", "Interface Incompatibility", "Subsystem interfaces don't work as specified", 2, 2, "Mitigate", "Formal ICD reviews; interface testing with stubs/mocks early in development"),
            ("T5", "Algorithm / Model Accuracy", "ML/control algorithms don't achieve target accuracy", 2, 3, "Mitigate", "Use simulation environment; define minimum acceptable metrics; plan multiple algorithm iterations"),
        ],
        "Schedule Risks": [
            ("S1", "Component Lead Times", "Critical components have long or unpredictable lead times", 3, 3, "Mitigate", "Order long-lead items immediately; identify alternate suppliers; maintain buffer stock"),
            ("S2", "Scope Creep", "Requirements grow beyond original scope", 3, 2, "Avoid", "Baseline requirements; formal change control process; regular scope reviews"),
            ("S3", "Resource Availability", "Key team members unavailable when needed", 2, 2, "Mitigate", "Cross-training; document knowledge; identify backup resources"),
            ("S4", "Testing Delays", "Testing takes longer than planned due to defects", 3, 2, "Mitigate", "Incremental testing; automated test suites; allocate 20-30% buffer for test phase"),
        ],
        "Cost Risks": [
            ("C1", "Hardware Cost Overrun", "Component costs exceed budget (price increases, redesigns)", 2, 2, "Mitigate", "Get firm quotes early; design for cost; have value-engineering plan"),
            ("C2", "Tooling & Licensing", "Unexpected tooling, software licenses, or certification costs", 2, 2, "Transfer", "Assess all tool requirements upfront; prefer open-source where possible"),
            ("C3", "Rework Costs", "Design flaws require expensive rework", 2, 3, "Mitigate", "Formal design reviews (PDR, CDR); simulation before fabrication; prototype early"),
        ],
        "External Risks": [
            ("E1", "Supply Chain Disruption", "Key supplier unable to deliver", 2, 3, "Mitigate", "Dual-source critical components; maintain safety stock; monitor supplier health"),
            ("E2", "Regulatory Changes", "New regulations impact design requirements", 1, 3, "Accept", "Monitor regulatory landscape; design with margin for compliance changes"),
            ("E3", "Vendor / Subcontractor Delay", "Third-party deliverables arrive late or substandard", 2, 2, "Mitigate", "Clear SLAs and milestones; regular vendor check-ins; penalty clauses"),
        ],
        "Safety Risks": [
            ("SF1", "Failure Mode Not Identified", "Undiscovered failure mode causes safety incident", 1, 4, "Mitigate", "Conduct FMEA/FMECA; hazard analysis; independent safety review"),
            ("SF2", "Insufficient Testing Coverage", "Safety-critical function not adequately tested", 1, 4, "Mitigate", "Requirements traceability matrix; 100% coverage for safety requirements; independent V&V"),
        ],
    }

    md.append("## Risk Register\n")

    for category, risks in risk_categories.items():
        md.append(f"### {category}\n")
        md.append("| ID | Risk | Description | Prob | Impact | Score | Strategy | Mitigation / Contingency |")
        md.append("|----|------|-------------|------|--------|-------|----------|--------------------------|")
        for rid, name, desc, prob, impact, strategy, mitigation in risks:
            score = prob * impact
            level = "Critical" if score >= 9 else "High" if score >= 6 else "Medium" if score >= 3 else "Low"
            md.append(f"| {rid} | {name} | {desc} | {prob} | {impact} | {score} ({level}) | {strategy} | {mitigation} |")
        md.append("")

    md.append("## Risk Monitoring Plan\n")
    md.append("| Review Frequency | Activity |")
    md.append("|-----------------|----------|")
    md.append("| Weekly | Review top-5 risks in standup |")
    md.append("| Bi-weekly | Update risk scores and mitigation status |")
    md.append("| Monthly | Full risk register review with stakeholders |")
    md.append("| At Phase Gates | Formal risk assessment before gate approval |")
    md.append("")

    md.append("<!-- COPILOT: Customize risks based on the specific project domain, technology -->")
    md.append("<!-- choices, and constraints. Add domain-specific risks and update probabilities -->")
    md.append("<!-- and impacts based on project context. -->")

    write_md(Path(output), "\n".join(md))


#  References Compiler 


def compile_references(research_dir: str, output: str) -> None:
    """Compile all references from research outputs into a single bibliography."""
    print(f"Compiling references from: {research_dir}")

    research_path = Path(research_dir)
    if not research_path.exists():
        print(f"  WARNING: Research directory not found: {research_dir}")
        write_md(Path(output), f"# References\n\n*No research data found in {research_dir}*\n")
        return

    web_refs = []
    paper_refs = []

    # Collect web search results
    for json_file in sorted(research_path.glob("web_*.json")):
        data = load_json_safe(json_file)
        for item in data.get("results", []):
            if item.get("url"):
                web_refs.append({
                    "title": item.get("title", "Untitled"),
                    "url": item.get("url"),
                    "source": item.get("source", ""),
                    "snippet": item.get("snippet", ""),
                    "mode": data.get("mode", "web"),
                    "accessed": data.get("timestamp", "")[:10],
                })

    # Collect academic papers
    for json_file in sorted(research_path.glob("papers_*.json")):
        data = load_json_safe(json_file)
        for paper in data.get("papers", []):
            paper_refs.append(paper)

    # Deduplicate
    seen_urls = set()
    unique_web = []
    for ref in web_refs:
        if ref["url"] not in seen_urls:
            seen_urls.add(ref["url"])
            unique_web.append(ref)

    seen_dois = set()
    unique_papers = []
    for ref in paper_refs:
        key = ref.get("doi") or ref.get("title", "")[:50].lower()
        if key and key not in seen_dois:
            seen_dois.add(key)
            unique_papers.append(ref)

    md = []
    md.append(f"# References & Bibliography")
    md.append(f"\n*Compiled: {today_str()}*")
    md.append(f"*Academic Papers: {len(unique_papers)} | Web Resources: {len(unique_web)}*\n")
    md.append("---\n")

    # Academic references
    if unique_papers:
        md.append("## Academic Papers\n")
        for i, p in enumerate(unique_papers, 1):
            authors = p.get("authors", [])
            author_str = ", ".join(authors[:3])
            if len(authors) > 3:
                author_str += " et al."
            year = p.get("year", "n.d.")
            title = p.get("title", "Untitled")
            venue = p.get("venue", "")
            doi = p.get("doi")
            url = p.get("url", "")
            arxiv = p.get("arxiv_id")
            citations = p.get("citation_count", 0)

            md.append(f"**[{i}]** {author_str} ({year}). *{title}*. {venue}.")
            if doi:
                md.append(f"  DOI: [{doi}](https://doi.org/{doi})")
            elif arxiv:
                md.append(f"  arXiv: [{arxiv}](https://arxiv.org/abs/{arxiv})")
            elif url:
                md.append(f"  URL: [{url}]({url})")
            if citations:
                md.append(f"  Citations: {citations}")
            md.append("")

    # Web references
    if unique_web:
        md.append("## Web Resources\n")
        for i, ref in enumerate(unique_web, 1):
            title = ref.get("title", "Untitled")
            url = ref.get("url")
            source = ref.get("source", "")
            accessed = ref.get("accessed", today_str()[:10])
            snippet = ref.get("snippet", "")

            md.append(f"**[W{i}]** [{title}]({url})")
            if source:
                md.append(f"  Source: {source}")
            if accessed:
                md.append(f"  Accessed: {accessed}")
            if snippet:
                md.append(f"  > {snippet[:200]}")
            md.append("")

    if not unique_papers and not unique_web:
        md.append("*No references collected yet. Run research phase first.*\n")

    write_md(Path(output), "\n".join(md))


#  Master Plan Compiler 


def compile_project_plan(project_name: str, project_dir: str, output: str) -> None:
    """Compile all deliverables into a master project plan document."""
    print(f"Compiling master project plan for: {project_name}")

    pdir = Path(project_dir)

    md = []
    md.append(f"# Technical Project Plan — {project_name}")
    md.append(f"\n*Generated: {today_str()}*")
    md.append(f"*Document Version: 1.0 (Draft)*\n")
    md.append("---\n")

    # Table of Contents
    md.append("## Table of Contents\n")
    toc = [
        "1. [Executive Summary](#1-executive-summary)",
        "2. [Project Scope & Objectives](#2-project-scope--objectives)",
        "3. [Requirements Summary](#3-requirements-summary)",
        "4. [Research Findings](#4-research-findings)",
        "5. [System Architecture](#5-system-architecture)",
        "6. [Work Breakdown Structure](#6-work-breakdown-structure)",
        "7. [Project Schedule](#7-project-schedule)",
        "8. [Risk Register](#8-risk-register)",
        "9. [Resource Plan](#9-resource-plan)",
        "10. [Quality Plan](#10-quality-plan)",
        "11. [Communication Plan](#11-communication-plan)",
        "12. [References](#12-references)",
    ]
    for item in toc:
        md.append(item)
    md.append("")

    # Section 1: Executive Summary
    md.append("## 1. Executive Summary\n")
    md.append("<!-- COPILOT: Write executive summary covering project purpose, key deliverables, -->")
    md.append("<!-- timeline, budget, and critical success factors. Keep to ~300 words. -->")
    md.append("\n**[To be written by Copilot based on all sections below]**\n")

    # Section 2: Scope & Objectives
    md.append("## 2. Project Scope & Objectives\n")
    md.append("<!-- COPILOT: Define project scope, objectives, success criteria, and exclusions -->")
    md.append("<!-- based on user-provided requirements and constraints. -->")
    md.append("\n**[To be written by Copilot based on user requirements]**\n")

    # Section 3: Requirements
    md.append("## 3. Requirements Summary\n")
    md.append("### 3.1 Functional Requirements\n")
    md.append("<!-- COPILOT: List functional requirements extracted from user input -->")
    md.append("\n### 3.2 Non-Functional Requirements\n")
    md.append("<!-- COPILOT: List NFRs (performance, reliability, safety, etc.) -->")
    md.append("\n### 3.3 Constraints\n")
    md.append("<!-- COPILOT: List constraints (budget, timeline, team, regulatory) -->")
    md.append("")

    # Section 4: Research Findings
    md.append("## 4. Research Findings\n")
    research_file = pdir / "research_summary.md"
    if research_file.exists():
        with open(research_file, "r", encoding="utf-8") as f:
            content = f.read()
        # Include research but skip the title
        lines = content.split("\n")
        for line in lines:
            if not line.startswith("# "):
                md.append(line)
    else:
        md.append("<!-- COPILOT: Synthesize research findings from web search and paper analysis -->")
        md.append("<!-- Include: technology landscape, standards, prior art, key academic findings -->")
        md.append("\n**[To be written after research phase]**\n")

    # Section 5: System Architecture
    md.append("\n## 5. System Architecture\n")
    arch_file = pdir / "system_architecture.md"
    if arch_file.exists():
        with open(arch_file, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.split("\n")
        for line in lines:
            if not line.startswith("# "):
                md.append(line)
    else:
        md.append("<!-- COPILOT: Design system architecture with Mermaid diagrams -->")
        md.append("<!-- Include: context diagram, component diagram, HW-SW partitioning -->")
        md.append("\n**[To be designed based on requirements and research]**\n")

    # Section 6: WBS
    md.append("\n## 6. Work Breakdown Structure\n")
    wbs_file = pdir / "wbs.md"
    if wbs_file.exists():
        with open(wbs_file, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.split("\n")
        for line in lines:
            if not line.startswith("# "):
                md.append(line)
    else:
        md.append("*See [wbs.md](wbs.md) — run generate_project_plan.py --mode wbs to generate*\n")

    # Section 7: Schedule
    md.append("\n## 7. Project Schedule\n")
    gantt_file = pdir / "gantt_chart.md"
    if gantt_file.exists():
        with open(gantt_file, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.split("\n")
        for line in lines:
            if not line.startswith("# "):
                md.append(line)
    else:
        md.append("*See [gantt_chart.md](gantt_chart.md) — run generate_project_plan.py --mode gantt to generate*\n")

    # Section 8: Risks
    md.append("\n## 8. Risk Register\n")
    risk_file = pdir / "risk_register.md"
    if risk_file.exists():
        with open(risk_file, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.split("\n")
        for line in lines:
            if not line.startswith("# "):
                md.append(line)
    else:
        md.append("*See [risk_register.md](risk_register.md) — run generate_project_plan.py --mode risks to generate*\n")

    # Section 9: Resource Plan
    md.append("\n## 9. Resource Plan\n")
    md.append("<!-- COPILOT: Create resource plan based on WBS and team constraints -->")
    md.append("<!-- Include: team structure, roles, skills needed, allocation percentage -->")
    md.append("\n### 9.1 Team Structure\n")
    md.append("| Role | Responsibility | Allocation | Skills Required |")
    md.append("|------|---------------|------------|-----------------|")
    md.append("| Project Lead | Overall project management, stakeholder communication | 100% | Systems engineering, PM |")
    md.append("| Systems Engineer | Architecture, integration, V&V | 100% | Systems design, multi-domain |")
    md.append("| HW Engineer | Electronics design, PCB, prototyping | 100% | EE, PCB design, DFM |")
    md.append("| SW Engineer | Firmware, application software | 100% | Embedded C/C++, RTOS |")
    md.append("| Test Engineer | Test planning, execution, automation | 50-100% | Test automation, HIL |")
    md.append("")

    # Section 10: Quality Plan
    md.append("\n## 10. Quality Plan\n")
    md.append("### 10.1 Verification Approach (V-Model)\n")
    md.append("`mermaid")
    md.append("graph LR")
    md.append("    A[Requirements] --> B[System Design]")
    md.append("    B --> C[Detailed Design]")
    md.append("    C --> D[Implementation]")
    md.append("    D --> E[Unit Testing]")
    md.append("    E --> F[Integration Testing]")
    md.append("    F --> G[System Testing]")
    md.append("    G --> H[Acceptance Testing]")
    md.append("    A -.-> H")
    md.append("    B -.-> G")
    md.append("    C -.-> F")
    md.append("`\n")
    md.append("### 10.2 Review Gates\n")
    md.append("| Gate | Purpose | Entry Criteria |")
    md.append("|------|---------|---------------|")
    md.append("| SRR (System Requirements Review) | Validate requirements completeness | All stakeholder needs captured |")
    md.append("| PDR (Preliminary Design Review) | Review system architecture | Architecture documented, trade studies complete |")
    md.append("| CDR (Critical Design Review) | Review detailed design | Detailed design complete, all interfaces defined |")
    md.append("| TRR (Test Readiness Review) | Confirm ready for V&V | All tests written, test environment ready |")
    md.append("| PRR (Production Readiness Review) | Ready for production | All V&V passed, production docs ready |")
    md.append("")

    # Section 11: Communication Plan
    md.append("\n## 11. Communication Plan\n")
    md.append("| Meeting | Frequency | Attendees | Purpose |")
    md.append("|---------|-----------|-----------|---------|")
    md.append("| Daily Standup | Daily | Core team | Status, blockers |")
    md.append("| Technical Review | Weekly | Engineering team | Design decisions, technical issues |")
    md.append("| Stakeholder Update | Bi-weekly | PM + stakeholders | Progress, risks, decisions needed |")
    md.append("| Phase Gate Review | Per milestone | All + reviewers | Formal go/no-go decision |")
    md.append("")

    # Section 12: References
    md.append("\n## 12. References\n")
    ref_file = pdir / "references.md"
    if ref_file.exists():
        with open(ref_file, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.split("\n")
        for line in lines:
            if not line.startswith("# "):
                md.append(line)
    else:
        md.append("*See [references.md](references.md) — run generate_project_plan.py --mode references to compile*\n")

    md.append("\n---\n")
    md.append(f"*End of Technical Project Plan — {project_name}*")

    write_md(Path(output), "\n".join(md))


#  CLI 


def main():
    parser = argparse.ArgumentParser(
        description="Technical Project Plan Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--mode", required=True,
                        choices=["wbs", "gantt", "risks", "references", "compile"],
                        help="Generation mode")
    parser.add_argument("--project-name", required=True, help="Name of the project")
    parser.add_argument("--requirements", help="Path to parsed requirements JSON")
    parser.add_argument("--wbs", help="Path to WBS markdown (for gantt mode)")
    parser.add_argument("--start-date", help="Project start date YYYY-MM-DD (for gantt mode)")
    parser.add_argument("--domain", help="Project domain (for risks mode)")
    parser.add_argument("--research-dir", help="Research data directory (for references mode)")
    parser.add_argument("--project-dir", help="Project deliverables directory (for compile mode)")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()

    if args.mode == "wbs":
        generate_wbs(args.project_name, args.requirements, args.output)
    elif args.mode == "gantt":
        start = args.start_date or datetime.now().strftime("%Y-%m-%d")
        generate_gantt(args.project_name, args.wbs, start, args.output)
    elif args.mode == "risks":
        domain = args.domain or "systems engineering"
        generate_risks(args.project_name, domain, args.output)
    elif args.mode == "references":
        rdir = args.research_dir or f".tmp/{slugify(args.project_name)}/"
        compile_references(rdir, args.output)
    elif args.mode == "compile":
        pdir = args.project_dir or f"outputs/{slugify(args.project_name)}/"
        compile_project_plan(args.project_name, pdir, args.output)


if __name__ == "__main__":
    main()
