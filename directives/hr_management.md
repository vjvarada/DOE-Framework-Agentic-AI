# HR Management Directive

> SOP for job descriptions, resume evaluation, candidate research, and HR document generation at Fracktal Works.

## Overview

This agent handles core HR workflows for Fracktal Works Pvt. Ltd — a 3D printing and digital manufacturing company based in Bangalore, India. The agent can create job descriptions, parse and evaluate resumes, research candidates online, and generate HR documents.

## Company Profile

- **Company:** Fracktal Works Pvt. Ltd
- **Industry:** 3D Printing / Digital Manufacturing / Additive Manufacturing
- **Founded:** 2013 at Manipal Institute of Technology
- **Location:** Bangalore, India
- **CEO:** Vijay Raghav Varada
- **Co-founder:** Rohit Asil
- **Website:** https://fracktal.in
- **Mission:** Empower sustainable development through Digital Fabrication & 3D Printing
- **Vision:** High-quality affordable manufacturing within the reach of every individual

### Products
- **Snowflake** — High-precision desktop 3D printer
- **Julia** — Flagship FDM 3D printer series
- **Dragon** — Large-format FDM 3D printer
- **Twin Dragon** — Dual-material FDM printer
- **Volterra** — Industrial FDM printer
- **Apollo SLS** — Production-grade Selective Laser Sintering printer
- **MDS-1 Material Dryer** — Filament moisture control
- **PrintStick** — Bed adhesion solution

### Services
- FDM, SLS, HP MJF, SLA, Vacuum Casting 3D printing services
- Engineering services (design, reverse engineering, quality assurance)
- Consulting services

### Key Technical Domains
- Mechanical Engineering (3D printer design, CAD, FEA, DFM)
- Embedded Systems (firmware, PCB design, motor control, sensors)
- Software Engineering (slicer software — Fracktory, cloud platforms, IoT)
- Materials Science (polymer science, print parameter optimization)
- Manufacturing (assembly, QA, production planning)
- Service Engineering (installation, calibration, customer training)

## Workflows

### 1. Create Job Description

**Trigger:** User requests a JD for a specific role

**Steps:**
1. Gather from user: job title, department, level (junior/mid/senior/lead), key responsibilities, required skills
2. Optionally research salary benchmarks: `python execution/research_candidate.py --mode salary-benchmark --role "<title>" --location "Bangalore"`
3. Generate JD: `python execution/generate_job_description.py --title "<title>" --department "<dept>" --level "<level>" --output ".tmp/jds/"`
4. In Copilot mode: use `--copilot` flag — script outputs a prompt, Copilot writes the JD content
5. Review with user, iterate
6. Final output: Google Doc (`create_google_doc.py`) or PDF (`generate_pdf.py`)

**JD Structure:**
- Company overview (use Fracktal Works boilerplate)
- Role summary
- Key responsibilities (5-10 bullet points)
- Required qualifications
- Preferred qualifications
- Technical skills required
- Soft skills
- What we offer / Benefits
- Location & work arrangement
- Application instructions

### 2. Evaluate Resumes / Candidates

**Trigger:** User provides PDF resumes for evaluation

**Steps:**
1. User places PDFs in `.tmp/resumes/` or provides file paths
2. Parse each resume: `python execution/parse_resume.py --input "<path>" --output ".tmp/parsed/"`
3. If a JD exists, evaluate fit: `python execution/evaluate_candidate.py --resume ".tmp/parsed/<name>.json" --jd ".tmp/jds/<role>.json" --output ".tmp/evaluations/"`
4. In Copilot mode: Copilot reviews parsed data and writes detailed evaluation
5. Optionally research candidate: `python execution/research_candidate.py --name "<name>" --current-company "<company>"`
6. Generate evaluation report (Google Doc or PDF)

**Evaluation Criteria:**
- Technical skills match (0-10)
- Experience relevance (0-10)
- Education fit (0-10)
- Industry alignment (bonus for manufacturing, robotics, 3D printing)
- Cultural indicators (startup experience, innovation, hands-on)
- Red flags (gaps, inconsistencies, job-hopping)
- Overall recommendation: Strong Hire / Hire / Maybe / No Hire

### 3. Research Candidates Online

**Trigger:** User wants background info on a candidate

**Steps:**
1. Search online: `python execution/research_candidate.py --name "<name>" --current-company "<company>" --role "<role>"`
2. Searches LinkedIn profiles, GitHub repos, publications, patents, news mentions
3. Compiles research summary
4. In Copilot mode: Copilot synthesizes findings

**Privacy Note:** Only use publicly available information. Do not attempt to access private accounts or restricted data.

### 4. Generate HR Documents

**Trigger:** User needs an offer letter, evaluation report, policy document, etc.

**Document Types:**
- **Offer Letter**: `python execution/generate_pdf.py --type offer-letter --data ".tmp/offer_data.json"`
- **Job Description PDF**: `python execution/generate_pdf.py --type job-description --data ".tmp/jds/<role>.json"`
- **Evaluation Report**: `python execution/generate_pdf.py --type evaluation-report --data ".tmp/evaluations/<candidate>.json"`
- **Interview Scorecard**: `python execution/generate_pdf.py --type interview-scorecard --data ".tmp/scorecard_data.json"`
- **Google Doc versions**: Use `create_google_doc.py` for editable cloud documents

### 5. HR Pipeline Tracking

**Trigger:** User wants to track candidates or hiring pipeline

**Steps:**
1. Create/update tracking sheet: `python execution/append_to_sheet.py --sheet-id "<id>" --data "<json>"`
2. Read pipeline status: `python execution/read_sheet.py --sheet-id "<id>" --range "<range>"`
3. Update candidate status: `python execution/update_sheet.py --sheet-id "<id>" --range "<range>" --data "<json>"`

**Sheet Columns:** Name, Email, Phone, Role Applied, Resume Link, Parse Score, Evaluation Score, Stage (Applied/Screened/Interview/Offer/Hired/Rejected), Notes, Date

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes | Google OAuth for Docs/Sheets |
| `SERPAPI_API_KEY` | Recommended | Online candidate research & salary benchmarks |
| `OPENAI_API_KEY` | Optional | Only for standalone mode |
| `ANTHROPIC_API_KEY` | Optional | Only for standalone mode |

## Edge Cases & Lessons Learned

- **Non-standard resume formats:** Some resumes are image-based PDFs (scanned). PyMuPDF may return empty text. Fall back to pdfplumber, then inform user if OCR is needed.
- **International resumes:** Name parsing varies by culture. Don't assume first-last name format.
- **Salary data:** SerpAPI salary benchmarks are approximations. Always note they're market estimates, not binding.
- **Confidentiality:** Never log or store candidate PII in memory database. Use `.tmp/` only, which is gitignored.
- **Indian labor law:** Offer letters should reference appointment terms per Shops & Establishments Act. Include probation period, notice period, at-will clauses per Indian norms.

## Output Locations

- **JDs:** `.tmp/jds/` (intermediate) → Google Docs / PDF (deliverable)
- **Parsed resumes:** `.tmp/parsed/` (intermediate, JSON)
- **Evaluations:** `.tmp/evaluations/` (intermediate) → Google Docs / PDF (deliverable)
- **Research reports:** `.tmp/research/` (intermediate)
- **Final documents:** Google Docs (cloud) or `.tmp/documents/` (PDF)
