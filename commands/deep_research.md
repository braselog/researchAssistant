# /deep_research Command

> Conduct a thorough literature search on a topic with verified citations.
> **CRITICAL**: Never fabricate citations. Every claim must have a verifiable source.

## When to Use
- Starting a new project (research core concepts)
- Exploring methodology options
- Understanding the current state of a field
- Finding prior work on a specific technique

## Usage
```
/deep_research [topic]
/deep_research normalization methods for RNA-seq
/deep_research machine learning in proteomics
```

## The 5-Step Literature Review Process

Follow this framework for rigorous, reproducible literature reviews:

```
1. DEFINE SCOPE    → What are we looking for? Set boundaries.
2. SEARCH          → Systematic, documented search across databases.
3. EVALUATE        → Assess source quality and relevance.
4. SYNTHESIZE      → Identify themes, patterns, and gaps.
5. DOCUMENT        → Write findings with proper citations.
```

## Execution Steps

### 1. Understand the Research Need (Define Scope)

If topic is vague, ask clarifying questions:
- "What specific aspect of [topic] are you most interested in?"
- "Are you looking for methodological approaches, theoretical background, or applications?"
- "Any specific time range? (e.g., last 5 years, seminal works)"

### 2. Generate Search Strategy

Break the topic into searchable concepts:

```markdown
## Search Strategy for: [Topic]

### Core Concepts
1. [Primary concept] - synonyms: [alternatives]
2. [Secondary concept] - synonyms: [alternatives]
3. [Methodological aspect]

### Search Queries
- "[concept1] AND [concept2]"
- "[method] in [application domain]"
- "review [topic]" (for overview papers)

### Key Databases
- PubMed (biomedical)
- arXiv (computational, preprints)
- Google Scholar (broad)
- Semantic Scholar (AI-enhanced)
```

### 3. Evaluate Sources

Apply the ACRAP criteria to each source:

| Criterion | Questions to Ask |
|-----------|------------------|
| **Authority** | Who wrote it? What are their credentials? Institutional affiliation? |
| **Currency** | When published? Is it current for this field? (Generally <5 years, seminal works excepted) |
| **Relevance** | Does it directly address the research question? |
| **Accuracy** | Is it peer-reviewed? Are claims supported by evidence? |
| **Purpose** | Why was it written? Any funding bias or conflicts of interest? |

**Quick Assessment:**
- ✅ High quality: Peer-reviewed, reputable journal, clear methodology
- ⚠️ Use with caution: Preprints, conference papers, older works
- ❌ Avoid: Non-peer-reviewed, predatory journals, unsupported claims

### 4. Conduct Research

**CRITICAL RULES:**
1. ✅ Only include claims with verifiable sources
2. ✅ Format citations properly (Author et al., Year)
3. ✅ Include DOI or URL when available
4. ❌ NEVER fabricate or guess citations
5. ❌ NEVER make up author names, years, or findings
6. ✅ If no source exists, explicitly state: "Gap identified: No literature found on [specific topic]"
7. ✅ If uncertain, say: "Limited sources found. Manual verification recommended."

### 4. Organize Findings

Structure the output as:

```markdown
# Literature Review: [Topic]

## Executive Summary
[2-3 sentence overview of the field]

## Current State of the Field

### [Theme 1]
[Synthesized findings with citations]

Key findings:
- Finding 1 (Author et al., Year)
- Finding 2 (Author et al., Year)

### [Theme 2]
[Synthesized findings]

### Methodological Approaches
[What methods are commonly used]

### Gaps in the Literature
- Gap 1: [What's missing or unexplored]
- Gap 2: [Contradictions or debates]

## Seminal Works
[Important foundational papers that should be cited]

## Recent Advances (Last 2-3 years)
[Most current developments]

## Implications for This Project
[How this literature relates to the user's aims]

## References

[Full BibTeX entries for all citations]
```

### Organizational Structure Options

Choose the structure that best fits the topic:

| Structure | Best For | Example |
|-----------|----------|----------|
| **Chronological** | Historical development, evolution of ideas | "1980s early work → 2000s key advances → 2020s current state" |
| **Thematic** | Multiple subtopics, most common choice | "Theme 1: Methods, Theme 2: Applications, Theme 3: Limitations" |
| **Methodological** | Comparing research approaches | "Quantitative → Qualitative → Mixed methods" |
| **Theoretical** | Comparing explanatory frameworks | "Theory A perspective → Theory B → Integration" |

### Common Literature Review Mistakes to Avoid

1. **Summarizing instead of synthesizing**
   - ❌ "Smith (2020) found X. Jones (2021) found Y. Lee (2022) found Z."
   - ✅ "While early work focused on X (Smith, 2020), recent studies reveal a broader pattern of Y and Z (Jones, 2021; Lee, 2022)."

2. **Imbalanced coverage**
   - Include studies that contradict your position
   - Represent the full landscape of evidence

3. **Missing recent publications**
   - Aim for >50% of citations from last 5 years
   - Seminal older works are acceptable exceptions

4. **Unclear connection to your study**
   - Always connect back to your research question
   - End each section with: "This is relevant because..."

5. **Citation strings without synthesis**
   - ❌ "Many studies support this (A, 2020; B, 2021; C, 2022; D, 2023; E, 2023)."
   - ✅ "This finding is well-established, with consistent support across methodologies (A, 2020; B, 2021) and populations (C, 2022; D, 2023)."

### 5. Save Outputs

Save to `.research/literature/`:
- `[topic-slug].md` - The literature summary
- `[topic-slug].bib` - BibTeX citations

Example:
```
.research/literature/
├── rna-seq-normalization.md
└── rna-seq-normalization.bib
```

### 6. Document Search for Reproducibility (PRISMA-style)

For systematic reviews or when rigor matters, document:

```markdown
## Search Documentation

**Date of search**: YYYY-MM-DD
**Databases searched**: [List all]

| Database | Search String | Results | After Dedup |
|----------|---------------|---------|-------------|
| PubMed | "term1" AND "term2" | 142 | 98 |
| Scopus | ... | ... | ... |
| arXiv | ... | ... | ... |

**Filters applied**: [Date range, language, article type]
**Inclusion criteria**: [What was included]
**Exclusion criteria**: [What was excluded]
**Total unique sources reviewed**: [N]
**Sources included in final review**: [N]
```

### Avoiding Bias in Literature Review

- ✅ Search multiple databases (not just one)
- ✅ Include grey literature when appropriate (theses, preprints, reports)
- ✅ Seek studies with negative/null findings
- ✅ Consider publication bias (positive results are over-published)
- ✅ Look for non-English sources if possible
- ✅ Document why sources were excluded
- ❌ Don't cherry-pick sources that support your hypothesis
- ❌ Don't ignore contradictory evidence

### 7. Prompt Next Steps

After completing:
```
Literature review saved to .research/literature/[topic].md

Suggested next steps:
A) Run /write_background to draft your background section
B) Run /deep_research on another topic: [suggest related topic]
C) Review the findings and refine your project aims

Would you like to explore any of these sources in more detail?
```

## Citation Format Standards

### In-Text Citations
- Single author: (Smith, 2023)
- Two authors: (Smith & Jones, 2023)
- Three+ authors: (Smith et al., 2023)
- Multiple citations: (Smith, 2023; Jones, 2022)

### BibTeX Format
```bibtex
@article{smith2023keyword,
  author = {Smith, John and Jones, Jane and Williams, Bob},
  title = {Title of the Paper},
  journal = {Journal Name},
  year = {2023},
  volume = {10},
  number = {2},
  pages = {123-145},
  doi = {10.1234/example.doi}
}
```

## Handling Uncertainty

### When sources are limited:
```
⚠️ Limited sources found on [specific topic].
Available sources cover [related area] but not [specific aspect].
Recommend:
- Manual search in [specific database]
- Consultation with domain expert
- This may represent a gap in the field
```

### When sources conflict:
```
📊 Conflicting findings in the literature:
- Position A: [claim] (Author1, Year)
- Position B: [opposing claim] (Author2, Year)
Current consensus appears to favor [position] based on [evidence].
```

### When no sources found:
```
🔍 Gap identified: No peer-reviewed literature found on [topic].
This could mean:
- Novel research opportunity
- Need for different search terms
- Topic may be covered under different terminology
Suggested alternative searches: [alternatives]
```

## Quality Checks

Before finalizing, verify:
- [ ] Every factual claim has a citation
- [ ] All citations are real and verifiable
- [ ] BibTeX entries are complete
- [ ] DOIs are included where available
- [ ] No made-up author names or publication details
- [ ] Gaps and limitations are explicitly stated

## Related Commands

- `/write_background` - Use literature to draft background section
- `/next` - Get next suggested step
- Run again with new topic for additional literature

## Example Output

```markdown
# Literature Review: Normalization Methods for RNA-seq

## Executive Summary
RNA-seq data normalization is essential for accurate differential expression analysis. Multiple methods exist with different assumptions about data distribution and sources of technical variation.

## Current State of the Field

### Total Count Normalization
The simplest approach scales counts by total library size (Mortazavi et al., 2008). While computationally efficient, this method assumes similar total RNA content across samples, which may not hold in all experimental designs.

### TMM and RLE Methods
Trimmed Mean of M-values (TMM) (Robinson & Oshlack, 2010) and Relative Log Expression (RLE) (Anders & Huber, 2010) address compositional bias by identifying stable reference genes. These methods are implemented in edgeR and DESeq2 respectively.

Key findings:
- TMM is robust to outliers (Robinson & Oshlack, 2010)
- RLE performs well with high replicate counts (Love et al., 2014)

### Gaps in the Literature
- Gap identified: Limited comparison studies for single-cell RNA-seq normalization
- Ongoing debate: Best practices for cross-species comparisons

## References

@article{robinson2010tmm,
  author = {Robinson, Mark D and Oshlack, Alicia},
  title = {A scaling normalization method for differential expression analysis of RNA-seq data},
  journal = {Genome Biology},
  year = {2010},
  volume = {11},
  pages = {R25},
  doi = {10.1186/gb-2010-11-3-r25}
}

@article{anders2010deseq,
  author = {Anders, Simon and Huber, Wolfgang},
  title = {Differential expression analysis for sequence count data},
  journal = {Genome Biology},
  year = {2010},
  volume = {11},
  pages = {R106},
  doi = {10.1186/gb-2010-11-10-r106}
}
```
