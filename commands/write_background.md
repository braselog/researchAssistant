# /write_background Command

> Draft or update the background/introduction section based on literature in .research/literature/

## When to Use
- After completing `/deep_research` on core concepts
- When literature files exist but background.md is empty
- To update background after additional literature review

## Prerequisites
- At least one literature summary in `.research/literature/`
- Project aims defined in `.research/project_telos.md`

## Execution Steps

### 1. Gather Context

Read these files:
- `.research/project_telos.md` - Project aims and mission
- `.research/literature/*.md` - All literature summaries
- `.research/literature/*.bib` - All citations
- `manuscript/background.md` - Existing draft (if any)

### 2. Identify Structure

A well-structured background follows the **funnel model**:

```
┌─────────────────────────────────────────┐
│     BROAD: Field context and           │  ← Why does this field matter?
│     importance                          │
├─────────────────────────────────────────┤
│   NARROWER: Current approaches and      │  ← What's been done?
│   what's known                          │
├─────────────────────────────────────────┤
│  SPECIFIC: Gaps, limitations,           │  ← What's missing?
│  open questions                         │
├─────────────────────────────────────────┤
│ YOUR STUDY: How you address the gap     │  ← What are you doing?
└─────────────────────────────────────────┘
```

### 3. Background Section Template

```markdown
# Background

## [Field Context - 1-2 paragraphs]
<!-- Start broad: Why does this area matter? What's the big picture? -->
<!-- Include 2-4 citations to establish context -->

[Field] is critical for [reason]. Recent advances in [area] have enabled 
[capabilities] (Citation1, Year; Citation2, Year). However, significant 
challenges remain in [challenge area].

## [Current Approaches - 2-3 paragraphs]
<!-- What methods/approaches exist? What have others done? -->
<!-- Synthesize literature thematically, don't just list papers -->

Current approaches to [problem] fall into [N] categories. First, [approach 1]
has been widely used because [reason] (Citations). However, this approach
[limitation].

Second, [approach 2] addresses [specific aspect] by [method] (Citations).
While effective for [use case], this method [limitation or gap].

## [Gaps and Limitations - 1-2 paragraphs]
<!-- What's missing? What hasn't been adequately addressed? -->
<!-- This sets up your research question -->

Despite these advances, [gap 1] remains poorly understood. Additionally, 
[gap 2] has received limited attention, particularly in the context of 
[specific application].
```

### Types of Gaps

Identify which type of gap your study addresses:

1. **Knowledge gap**: "It is unknown whether..."
2. **Methodological gap**: "Previous studies have not used..."
3. **Population gap**: "No studies have examined this in..."
4. **Theoretical gap**: "No framework exists to explain..."
5. **Practical gap**: "Current approaches fail to address..."

### Gap Statement Templates

```markdown
- "Despite [what's known], [what's unknown]."
- "While previous work has [X], no studies have [Y]."
- "The relationship between [A] and [B] remains unclear."
- "Limited evidence exists regarding..."
- "A critical gap in our understanding is..."
```

### Research Question/Hypothesis Setup

**For Hypothesis-Driven Research:**
```markdown
"Based on [theoretical framework/previous findings], we hypothesized 
that [specific, testable prediction]. To test this, we [approach]."
```

**For Exploratory Research:**
```markdown
"The objective of this study was to [primary aim]. Specifically, we 
sought to: (1) [aim 1], (2) [aim 2], and (3) [aim 3]."
```

### Common Introduction Mistakes

1. **Too broad opening**
   - ❌ "Since the beginning of time, humans have wondered about..."
   - ✅ "[Specific topic] affects [specific population/process]..."

2. **Literature review too detailed**
   - Introduction ≠ full literature review
   - Include only what's needed to establish the gap

3. **Gap not clearly stated**
   - Make it explicit, not implied
   - Should appear before study aims

4. **Objectives mismatch methods**
   - Every stated objective must be addressed in Methods/Results

5. **Excessive length**
   - Typical length: 500-1000 words (3-5 paragraphs)
   - Follow journal guidelines

## [Your Contribution - 1 paragraph]
<!-- How does your work address these gaps? -->
<!-- State aims clearly without overpromising -->

In this study, we address [gap] by [approach]. Specifically, we [aim 1], 
[aim 2], and [aim 3]. Our approach differs from prior work by [key 
distinction].
```

### 4. Writing Guidelines

**DO:**
- Synthesize across sources (don't just summarize individual papers)
- Use present tense for established knowledge ("X is known to...")
- Use past tense for specific study findings ("Smith et al. found...")
- Connect ideas with transitions
- Build toward your research question logically
- Include 20-40 citations for a typical paper background

**DON'T:**
- List papers without connecting them ("Paper A did X. Paper B did Y.")
- Include citations without explanation
- Fabricate citations not in your .bib files
- Make claims without support
- Use jargon without defining it
- Front-load with history that doesn't connect to your work

### 5. Citation Density Guidelines

| Section | Citation Density |
|---------|------------------|
| Field context | High (establish foundation) |
| Current approaches | Very high (show you know the field) |
| Gaps and limitations | Medium (may include your reasoning) |
| Your contribution | Low to none (this is you, not literature) |

### 6. Generate Draft

Create or update `manuscript/background.md`:

```markdown
# Background

<!-- 
Draft generated by Research Assistant on [DATE]
Based on literature in: .research/literature/
Related aims: [list aims from project_telos.md]

⚠️ REVIEW CAREFULLY: 
- Verify all citations against your .bib files
- Add context specific to your project
- Adjust for target journal style
-->

[Generated content following template above]

---

## References Used
[List of .bib files consulted]

## Potential Gaps to Address
[Any areas where more literature may be needed]
```

### 7. Post-Draft Checks

Present these checks to the user:
```
Background draft created. Please review:

✓ Citations verified against .research/literature/*.bib
? Check: Does the funnel flow logically to your aims?
? Check: Are there areas needing additional literature?
? Check: Does this match your target journal's style?

Suggested next steps:
A) Review and edit manuscript/background.md
B) Run /deep_research on [suggested missing topic]
C) Proceed to /write_methods if pipeline is ready
```

## Example Output Section

```markdown
## Current Approaches to Gene Expression Normalization

Normalization of RNA-seq data is essential for accurate differential 
expression analysis, as raw count data reflects both biological variation 
and technical artifacts (Dillies et al., 2013). Several approaches have 
emerged to address this challenge.

**Library size normalization** scales counts by the total number of reads 
per sample (Mortazavi et al., 2008). While computationally simple, this 
approach assumes equal total RNA content across samples—an assumption 
that may be violated in many experimental designs, particularly those 
involving different cell types or treatment conditions.

**Reference-based methods** such as TMM (Robinson & Oshlack, 2010) and 
RLE (Anders & Huber, 2010) identify a set of stable reference features 
to compute scaling factors. These methods have become standard in tools 
like edgeR and DESeq2, demonstrating robust performance across diverse 
datasets (Love et al., 2014).

Despite the success of these methods for bulk RNA-seq, their application 
to **single-cell data** remains challenging due to high dropout rates 
and sparse count matrices (Kharchenko et al., 2014).
```

## Related Commands

- `/deep_research [topic]` - If more literature is needed
- `/write_methods` - Next manuscript section
- `/next` - Get suggestions for next steps
