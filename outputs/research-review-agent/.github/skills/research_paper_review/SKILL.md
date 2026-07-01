---
name: research_paper_review
description: >
  Migrated from directives/research_paper_review.md
when_to_use: "User asks about research paper review"
authority: read
cost_tier: 1
version: 0.1.0
---

# Create State-of-the-Art Review Paper

## Goal
Create a comprehensive state-of-the-art review paper in markdown format on a given research topic, properly citing academic papers with DOIs.

## When to Use
- User provides a research topic and wants a literature review
- User needs to understand the current state of research in a field
- User wants a structured summary of recent academic work with proper citations

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| Topic | Yes | The research topic to review |
| Depth | No | shallow (5-10 papers), medium (15-25 papers), deep (30+ papers). Default: medium |
| Focus Areas | No | Specific subtopics or angles to emphasize |
| Year Range | No | Publication years to filter. Default: last 5 years |
| Output Path | No | Where to save the review. Default: `.tmp/review_paper.md` |

## Outputs
- **Primary**: Markdown review paper with sections, summaries, and proper DOI citations
- **Secondary**: BibTeX file with all references
- **Intermediate**: Paper summaries in `.tmp/paper_summaries/`

## Workflow

### Phase 1: Paper Discovery

#### Step 1.1: Search for Papers
Use multiple sources to find relevant papers:

```bash
# Search Semantic Scholar (free, no API key needed for basic searches)
python execution/search_papers.py --topic "{topic}" --source semantic_scholar --limit 50

# Search CrossRef (free, no API key needed)
python execution/search_papers.py --topic "{topic}" --source crossref --limit 50

# Search arXiv (free, no API key needed)
python execution/search_papers.py --topic "{topic}" --source arxiv --limit 50

# Use Google Scholar via SerpAPI (requires API key)
python execution/search_papers.py --topic "{topic}" --source google_scholar --limit 50
```

Output: `.tmp/discovered_papers.json` with paper metadata including titles, authors, DOIs, abstracts, and URLs.

#### Step 1.2: Deduplicate and Rank
Papers are automatically deduplicated by DOI and ranked by:
- Citation count
- Publication date (newer = higher)
- Relevance score from search

### Phase 2: Paper Collection

#### Step 2.1: Check Paper Availability
For each paper, the system attempts to:
1. **Fetch from open access**: arXiv, PubMed Central, Unpaywall, CORE
2. **Fetch abstract only**: If full text unavailable

```bash
python execution/fetch_paper.py --doi "{doi}" --output ".tmp/papers/"
```

#### Step 2.2: Handle Paywalled Papers
If a paper is behind a paywall:

**IMPORTANT**: Inform the user which papers are paywalled and provide:
- DOI link
- Journal name
- Title

Ask user to either:
1. Provide the PDF in `.tmp/user_papers/`
2. Skip the paper
3. Use abstract-only summary

### Phase 3: Paper Processing

#### Step 3.1: Convert PDFs to Markdown
```bash
python execution/pdf_to_markdown.py --input ".tmp/papers/{filename}.pdf" --output ".tmp/paper_markdown/"
```

This extracts:
- Full text content
- Tables (as markdown tables)
- Figure captions
- Section headings

#### Step 3.2: Summarize Papers
For each paper, extract (Copilot does this directly):
- **Key contributions**: What novel ideas/methods does this paper introduce?
- **Methodology**: What approach/techniques are used?
- **Results**: What are the main findings?
- **Limitations**: What gaps or weaknesses exist?
- **Relevance**: How does this relate to the topic?

Save summaries to `.tmp/paper_summaries/{doi_slug}.md`

### Phase 4: Synthesis

#### Step 4.1: Identify Themes
Analyze all paper summaries to identify:
- Major research themes/approaches
- Chronological evolution
- Key debates/disagreements
- Gaps in the literature

#### Step 4.2: Create Review Structure
Standard structure:
1. **Abstract**: Brief overview of the review
2. **Introduction**: Problem statement, scope, methodology
3. **Background**: Foundational concepts
4. **Methodology/Taxonomy**: How papers are categorized
5. **State of the Art**: Main body organized by theme
6. **Discussion**: Synthesis, trends, gaps
7. **Conclusion**: Summary and future directions
8. **References**: DOI-linked bibliography

### Phase 5: Compilation

#### Step 5.1: Compile Review Paper
```bash
python execution/compile_review_paper.py \
    --summaries-dir ".tmp/paper_summaries/" \
    --output ".tmp/review_paper.md" \
    --bibtex ".tmp/references.bib"
```

The script creates the structure; Copilot writes the content sections.

#### Step 5.2: Format Citations
All citations use format: `(Author et al., Year)` with DOI links.

Example:
```markdown
Recent advances in transformer architectures have revolutionized NLP (Vaswani et al., 2017)[^1].

[^1]: Vaswani, A., et al. (2017). Attention is all you need. *NeurIPS*. DOI: [10.5555/3295222.3295349](https://doi.org/10.5555/3295222.3295349)
```

## Error Handling

### API Rate Limits
- Semantic Scholar: 100 requests/5 min (unauthenticated)
- CrossRef: Polite limit with email header
- arXiv: 1 request/3 seconds
- SerpAPI: Based on plan

**Solution**: Built-in rate limiting and caching in search_papers.py

### PDF Extraction Failures
If `pdf_to_markdown.py` fails:
1. Try alternative backend (PyMuPDF → pdfplumber → pdf2image+OCR)
2. Fall back to abstract-only summary
3. Log the issue and continue

### Missing DOIs
If a paper lacks a DOI:
- Try to find DOI via CrossRef API using title/authors
- Use alternative identifier (arXiv ID, PubMed ID)
- Create citation without DOI link

## Best Practices

### Quality Indicators
- Prioritize peer-reviewed papers over preprints
- Check citation count (high citations = influential)
- Verify recent papers for cutting-edge developments
- Include seminal/foundational papers even if older

### Citation Ethics
- Always include DOI when available
- Never fabricate citations
- Use exact paper titles
- Include all authors or "et al." for 3+

### Review Balance
- Cover multiple perspectives/approaches
- Note disagreements in the field
- Identify methodology variations
- Acknowledge limitations of the review itself

## Example Usage

**User**: "Create a review paper on 'Large Language Models for Code Generation'"

**Agent Actions**:
1. Search papers across all sources with keywords: "large language model", "code generation", "program synthesis", "neural code"
2. Collect top 25 most relevant/cited papers
3. Convert available PDFs to markdown
4. Summarize each paper's contributions
5. Identify themes: model architectures, training data, benchmarks, applications
6. Write review sections
7. Compile final markdown with DOIs

## Tool Reference

| Script | Purpose |
|--------|---------|
| `search_papers.py` | Discover papers from multiple sources |
| `fetch_paper.py` | Download papers from open access sources |
| `pdf_to_markdown.py` | Convert PDF to readable markdown |
| `compile_review_paper.py` | Structure and format the final review |

## Notes for Self-Improvement

- Update source APIs as they change
- Add new open access sources as discovered
- Track which papers consistently fail extraction
- Note journals with good open access policies
