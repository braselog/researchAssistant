---
name: statistical-analysis
description: Designs, executes, and reports statistical analyses grounded in the research question, data-generating process, experimental unit, and estimand. Use for /statistical_analysis or analytical design and interpretation questions.
---

# Statistical analysis

Define the question, estimand, outcome, predictors, independent unit, design, sampling process, and confirmatory versus exploratory status before selecting a method.

## Workflow
1. Inspect provenance, exclusions, missingness, dependence, confounders, and preprocessing.
2. Choose a model that matches the estimand and data-generating process, not a lookup table.
3. Specify contrasts, uncertainty estimates, validation, multiplicity handling, and sensitivity analyses.
4. Prevent leakage by separating fitting, tuning, feature selection, and evaluation at the correct grouping level.
5. Run diagnostics relevant to the chosen model and assess influential observations without automatic removal.
6. Report effect estimates with uncertainty and exact sample definitions; include p-values only where meaningful.
7. Save code, parameters, and machine-readable results when this is project work.

Do not infer causality without an identifying design, treat technical replicates as independent, perform post hoc power as evidence for a null result, or use generic effect-size labels as substitutes for domain relevance. State unresolved assumptions and limitations.
