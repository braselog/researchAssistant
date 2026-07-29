# Research Notes

This directory contains topical notes, ideas, hypotheses, and reference information that don't fit into tasks or activity logs.

## What Goes Here?

**Notes are for:**
- Ideas to explore later (not yet actionable tasks)
- Hypotheses under consideration
- Reference information (citations, URLs, concepts)
- Context about why something matters
- Questions to investigate

**Use activity.md for:** Completed work and decisions  
**Use tasks.md for:** Actionable items with clear done states

## Organization

Create topic-specific files as needed:

```
notes/
├── hypotheses.md         # Research hypotheses and theories
├── data-quality.md       # Observations about data issues/patterns
├── methodological.md     # Methods considerations
├── literature-gaps.md    # Missing citations or knowledge gaps
├── meeting-ideas.md      # Ideas from discussions
└── [custom-topic].md     # Any other topic
```

## Entry Format

```markdown
## [YYYY-MM-DD] [Title]

[Content/observation]

[Optional: Related to: [task/file/section]]
[Optional: See also: [other note]]
```

## Examples

### Hypothesis Note
```markdown
## 2026-01-09 Time Lag Hypothesis

Low correlation between X and Y might be due to unaccounted time lag effect. 
Consider testing lagged correlations (1-4 week delays).

Related to: analysis of correlation matrix in results/exploratory/
```

### Reference Note
```markdown
## 2026-01-09 Alternative Interpretation

Smith et al. (2024) found similar pattern but attributed it to sampling bias
rather than true effect. Check if our sampling strategy could introduce similar bias.

Citation: Smith et al. 2024, Journal of X, DOI:xxxxx
See also: methodological.md#sampling-strategy
```

### Data Observation
```markdown
## 2026-01-09 Outliers in Variable Z

Preprocessing revealed 5 outliers (>3 SD) in variable Z. 
- Not obvious data entry errors
- Could be real signal or measurement artifacts
- Concentrated in May-June timeframe

Related to: data/processed/cleaned_data.csv
```

---

*The Research Assistant uses this directory to remember context across sessions.*
*Create new topics as needed - stay organized but don't over-structure.*
