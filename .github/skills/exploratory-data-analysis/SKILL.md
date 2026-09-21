---
name: exploratory-data-analysis
description: Performs project-aware exploratory analysis that checks data structure, quality, provenance, distributions, dependence, and potential leakage before formal modelling. Use for /exploratory_data_analysis or when a dataset needs inspection.
---

# Exploratory data analysis

Start from the research question, data dictionary, provenance, experimental unit, sampling design, and downstream use. Never apply a generic plotting checklist without first understanding the data.

## Workflow
1. Load data without modifying source files and record the exact input path or version.
2. Verify dimensions, types, identifiers, units, sample alignment, duplicates, and expected cardinalities.
3. Examine missingness, censoring, impossible values, batch structure, and exclusions in context.
4. Summarize distributions and relationships at the correct independent-unit level.
5. Check repeated measures, clustering, technical replication, leakage, and confounding before group comparisons.
6. Investigate unusual observations without automatically deleting them.
7. Create only informative, reproducible figures and tables.
8. Save analysis code and derived outputs through the project workflow when requested.

Report verified observations separately from interpretations and recommended follow-up. Do not select inferential tests solely from normality tests or treat visual patterns as confirmed effects.
