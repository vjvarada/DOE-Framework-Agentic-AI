# Technical Project Planning Directive

## Goal
Create comprehensive technical project plans for hardware-software, systems engineering projects. This includes system architecture design, execution plans, Gantt charts, work breakdown structures (WBS), risk assessments, and full project management documentation — all backed by industry research, prior art analysis, and academic references.

## When to Use
- User provides high-level requirements and constraints for a technical project
- User needs a system architecture for a multi-disciplinary engineering project
- User wants an execution plan with milestones, dependencies, and timelines
- User needs a Gantt chart or work breakdown structure
- User wants research-backed recommendations for technology choices and architecture patterns

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| Project Name | Yes | Name/title of the project |
| Requirements | Yes | High-level functional and non-functional requirements |
| Constraints | No | Budget, timeline, team size, regulatory, technology constraints |
| Domain | No | Primary domain (e.g., embedded systems, IoT, robotics, aerospace, automotive) |
| Focus Areas | No | Specific areas to emphasize (e.g., reliability, real-time, safety-critical) |
| Output Path | No | Where to save deliverables. Default: `outputs/{project-slug}/` |
| Research Depth | No | shallow (quick), medium (standard), deep (extensive). Default: medium |

## Outputs

### Primary Deliverables (saved to `outputs/{project-slug}/`)
- **`project_plan.md`** — Master project plan document with all sections
- **`system_architecture.md`** — System architecture with diagrams (Mermaid)
- **`gantt_chart.md`** — Gantt chart in Mermaid format plus timeline tables
- **`wbs.md`** — Work Breakdown Structure
- **`risk_register.md`** — Risk assessment and mitigation strategies
- **`research_summary.md`** — Research findings with citations and links
- **`references.md`** — Full bibliography with URLs and DOIs

### Intermediate Files (in `.tmp/{project-slug}/`)
- Web search results JSON
- Academic paper metadata JSON
- Paper summaries
- Raw research notes

## Workflow

### Phase 1: Requirements Analysis

#### Step 1.1: Parse Requirements
Copilot analyzes the user's high-level requirements and extracts:
- **Functional Requirements (FR)**: What the system must do
- **Non-Functional Requirements (NFR)**: Performance, reliability, safety, scalability
- **Interface Requirements**: Hardware-software interfaces, communication protocols
- **Regulatory Requirements**: Standards compliance (ISO, IEC, MIL-STD, DO-178, etc.)
- **Constraints**: Budget, timeline, team, technology limitations

#### Step 1.2: Identify Research Queries
Based on requirements, generate targeted search queries for:
- System architecture patterns for the domain
- Technology choices and trade-offs
- Industry best practices and standards
- Similar project implementations (prior art)
- Academic research on key technical challenges

### Phase 2: Research & Prior Art Analysis

#### Step 2.1: Web Search for Industry Practices
```bash
# Search for industry practices, standards, similar projects
python execution/web_research.py --mode search --query "{domain} system architecture best practices" --num-results 15 --output ".tmp/{project-slug}/web_search_architecture.json"

# Search for technology comparisons and trade-offs
python execution/web_research.py --mode search --query "{key technology} vs {alternative} for {use case}" --num-results 10 --output ".tmp/{project-slug}/web_search_tech.json"

# Search for standards and compliance requirements
python execution/web_research.py --mode search --query "{domain} engineering standards compliance {ISO/IEC/etc}" --num-results 10 --output ".tmp/{project-slug}/web_search_standards.json"

# Search for prior art and reference architectures
python execution/web_research.py --mode prior-art --query "{project description}" --num-results 15 --output ".tmp/{project-slug}/web_search_prior_art.json"

# Search for news and recent developments
python execution/web_research.py --mode news --query "{domain} latest developments {year}" --num-results 10 --output ".tmp/{project-slug}/web_search_news.json"
```

#### Step 2.2: Academic Paper Search
```bash
# Search all academic databases for relevant papers
python execution/search_papers.py --topic "{key technical challenge}" --source all --limit 30 --output ".tmp/{project-slug}/papers_challenge.json"

# Search for architecture-specific papers
python execution/search_papers.py --topic "{domain} system architecture design" --source all --limit 20 --output ".tmp/{project-slug}/papers_architecture.json"

# Search for methodology papers
python execution/search_papers.py --topic "{methodology} engineering methodology" --source all --limit 15 --output ".tmp/{project-slug}/papers_methodology.json"
```

#### Step 2.3: Fetch and Process Key Papers
```bash
# Fetch top papers (open access)
python execution/fetch_paper.py --json ".tmp/{project-slug}/papers_challenge.json" --output ".tmp/{project-slug}/papers/" --limit 10

# Convert PDFs to markdown for reading
python execution/pdf_to_markdown.py --input ".tmp/{project-slug}/papers/" --output ".tmp/{project-slug}/paper_markdown/" --batch
```

#### Step 2.4: Synthesize Research
Copilot reads all research outputs and creates:
- **Technology landscape summary** with pros/cons of different approaches
- **Standards and compliance checklist** for the domain
- **Prior art analysis** showing what others have done
- **Key findings** from academic literature
- **Recommended approaches** with justification

Save to: `outputs/{project-slug}/research_summary.md`

### Phase 3: System Architecture Design

#### Step 3.1: High-Level Architecture
Copilot designs the system architecture including:
- **System context diagram** (Mermaid C4 model)
- **Component diagram** showing major subsystems
- **Hardware-software partitioning** decisions
- **Interface definitions** between subsystems
- **Communication protocols** and data flows

#### Step 3.2: Detailed Architecture
For each major subsystem:
- **Block diagram** (Mermaid)
- **Technology stack** selection with justification
- **Interface specifications**
- **Performance requirements allocation**
- **Trade-off analysis** with references to research

#### Step 3.3: Architecture Decisions Record (ADR)
Document key architecture decisions:
- **Context**: Why is this decision needed?
- **Options Considered**: What alternatives were evaluated?
- **Decision**: What was chosen and why?
- **Consequences**: What are the trade-offs?
- **References**: Links to supporting research/standards

Save to: `outputs/{project-slug}/system_architecture.md`

### Phase 4: Work Breakdown Structure (WBS)

#### Step 4.1: Generate WBS
```bash
python execution/generate_project_plan.py --mode wbs \
    --project-name "{project name}" \
    --requirements ".tmp/{project-slug}/parsed_requirements.json" \
    --output "outputs/{project-slug}/wbs.md"
```

The WBS includes:
- **Level 1**: Project phases (Research, Design, Implementation, Testing, Deployment)
- **Level 2**: Major deliverables per phase
- **Level 3**: Work packages (assignable tasks)
- **Level 4**: Activities (detailed tasks with effort estimates)

For systems engineering projects, typical phases include:
1. Concept & Requirements
2. System Architecture & Design
3. Hardware Development
4. Software Development
5. Integration & Test
6. Verification & Validation
7. Production & Deployment
8. Operations & Maintenance

#### Step 4.2: Effort Estimation
For each work package, estimate:
- **Optimistic (O)**: Best case
- **Most Likely (M)**: Normal case
- **Pessimistic (P)**: Worst case
- **PERT Estimate**: (O + 4M + P) / 6

### Phase 5: Project Schedule (Gantt Chart)

#### Step 5.1: Generate Gantt Chart
```bash
python execution/generate_project_plan.py --mode gantt \
    --project-name "{project name}" \
    --wbs "outputs/{project-slug}/wbs.md" \
    --start-date "{YYYY-MM-DD}" \
    --output "outputs/{project-slug}/gantt_chart.md"
```

The Gantt chart includes:
- **Mermaid Gantt diagram** (renders in markdown preview)
- **Milestone table** with dates and dependencies
- **Critical path** identification
- **Resource allocation** overview
- **Phase gates / review points**

#### Step 5.2: Dependency Analysis
Identify and document:
- **Finish-to-Start (FS)**: Task B can't start until Task A finishes
- **Start-to-Start (SS)**: Tasks can start together
- **Finish-to-Finish (FF)**: Tasks must finish together
- **External dependencies**: Vendor deliveries, regulatory approvals, etc.

Save to: `outputs/{project-slug}/gantt_chart.md`

### Phase 6: Risk Assessment

#### Step 6.1: Risk Identification
```bash
python execution/generate_project_plan.py --mode risks \
    --project-name "{project name}" \
    --domain "{domain}" \
    --output "outputs/{project-slug}/risk_register.md"
```

Risk categories for systems engineering:
- **Technical Risks**: Technology maturity, integration complexity, performance uncertainty
- **Schedule Risks**: Dependency delays, resource availability, scope creep
- **Cost Risks**: Hardware cost escalation, tooling requirements, licensing
- **External Risks**: Supply chain, regulatory changes, vendor reliability
- **Safety Risks**: Failure modes, hazard analysis (for safety-critical systems)

#### Step 6.2: Risk Analysis
For each risk:
- **Probability**: Low (1) / Medium (2) / High (3)
- **Impact**: Low (1) / Medium (2) / High (3) / Critical (4)
- **Risk Score**: Probability × Impact
- **Mitigation Strategy**: Avoid, Transfer, Mitigate, Accept
- **Contingency Plan**: What to do if the risk materializes
- **Owner**: Who monitors this risk

Save to: `outputs/{project-slug}/risk_register.md`

### Phase 7: Compilation

#### Step 7.1: Compile Master Project Plan
```bash
python execution/generate_project_plan.py --mode compile \
    --project-name "{project name}" \
    --project-dir "outputs/{project-slug}/" \
    --output "outputs/{project-slug}/project_plan.md"
```

Master project plan structure:
1. **Executive Summary**
2. **Project Scope & Objectives**
3. **Requirements Summary** (FR, NFR, constraints)
4. **Research Findings** (key insights with citations)
5. **System Architecture** (with diagrams)
6. **Work Breakdown Structure**
7. **Project Schedule** (Gantt chart)
8. **Resource Plan**
9. **Risk Register**
10. **Quality Plan** (V&V approach)
11. **Communication Plan**
12. **References & Bibliography**

#### Step 7.2: Generate References
```bash
python execution/generate_project_plan.py --mode references \
    --research-dir ".tmp/{project-slug}/" \
    --output "outputs/{project-slug}/references.md"
```

All references include:
- Full citation (IEEE or APA format)
- DOI link (for academic papers)
- URL (for web resources)
- Access date
- Brief annotation of relevance

## Error Handling

### Web Search Failures
- If SerpAPI fails, fall back to academic search only
- Cache all search results for reuse
- Log which searches failed and why

### Paper Access Issues
- Report paywalled papers to user
- Use abstract-only summaries when full text unavailable
- Prioritize open-access papers

### Estimation Uncertainty
- Use PERT ranges instead of point estimates
- Flag high-uncertainty items for user review
- Include confidence levels in schedule

## Best Practices

### For Systems Engineering Projects
- Follow the V-Model for hardware-software co-development
- Include clear phase gates (SRR, PDR, CDR, TRR, etc.)
- Allocate explicit integration time (usually 20-30% of total)
- Plan for hardware-software interface testing early
- Consider supply chain lead times for hardware components

### For Multi-Disciplinary Teams
- Define clear interface ownership
- Include interface control documents (ICDs) in deliverables
- Plan concurrent engineering activities where possible
- Budget for cross-disciplinary reviews

### Research Quality
- Prioritize peer-reviewed sources over blogs
- Include standards documents (ISO, IEC, IEEE) when applicable
- Cross-reference multiple sources for key claims
- Note publication dates — technology moves fast

### Citation Format
All citations follow this format:
```markdown
According to recent research on embedded system architectures (Smith et al., 2024)[^1], the microservice pattern...

[^1]: Smith, J., et al. (2024). Embedded System Architecture Patterns for IoT. *IEEE Transactions on Industrial Informatics*. DOI: [10.1109/TII.2024.xxxxx](https://doi.org/10.1109/TII.2024.xxxxx)
```

Web resources:
```markdown
The AUTOSAR standard defines a layered architecture for automotive ECUs[^2].

[^2]: AUTOSAR Consortium. (2024). AUTOSAR Classic Platform. Retrieved from [https://www.autosar.org/](https://www.autosar.org/) (Accessed: 2025-01-15)
```

## Example Usage

**User**: "I need a project plan for an autonomous drone inspection system for power lines. It needs to fly autonomously along transmission lines, detect faults using computer vision, avoid obstacles with LiDAR, and report findings via cellular to a ground station. Budget is $500K, team of 6, 12-month timeline."

**Agent Actions**:
1. Parse requirements → FR (autonomous flight, CV fault detection, LiDAR avoidance, cellular comms), NFR (safety, reliability, range), Constraints ($500K, 6 people, 12 months)
2. Generate research queries → "autonomous drone inspection power line architecture", "UAV obstacle avoidance LiDAR systems", "computer vision power line fault detection", "drone cellular communication systems"
3. Web search for industry practices, similar systems, FAA regulations
4. Academic search for CV fault detection methods, autonomous navigation
5. Design system architecture (flight controller, CV module, LiDAR processing, comms, ground station)
6. Generate WBS for 12-month timeline with phase gates
7. Create Gantt chart with hardware procurement, SW development, integration testing
8. Assess risks (FAA regulatory, weather, CV accuracy, battery life)
9. Compile master project plan with all references

## Tool Reference

| Script | Purpose |
|--------|---------|
| `execution/web_research.py` | Web search for industry practices, prior art, standards, news |
| `execution/search_papers.py` | Search academic databases (Semantic Scholar, CrossRef, arXiv) |
| `execution/fetch_paper.py` | Download papers from open access sources |
| `execution/pdf_to_markdown.py` | Convert academic PDFs to readable markdown |
| `execution/generate_project_plan.py` | Generate WBS, Gantt charts, risk registers, compile plans |
