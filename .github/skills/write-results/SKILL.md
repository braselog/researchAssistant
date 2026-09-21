---
name: write-results
description: Drafts or updates results from current machine-readable outputs, statistics, tables, figures, and captions. Use for /write_results when results need to be written or checked against evidence.
---

# Write results from current evidence

Read the project aims, current outputs, analysis summaries, statistical results, figures, captions, relevant methods, and existing results text. Prefer machine-readable result artifacts over values copied into old prose.

Organize around scientific findings and aims, not file order. Report sample definitions, estimates, uncertainty, tests, effect sizes, and figure/table references as supported. Include null or contradictory findings relevant to the stated analyses. Keep interpretation proportionate and reserve broader mechanisms and implications for the discussion.

Never infer numbers from plotted pixels, fabricate missing statistics, or copy stale values from captions. Flag contradictions among outputs, captions, methods, and prose.


## Reproducibility gate and evidence map
Before editing manuscript text, determine whether relevant DVC stages and source outputs are current. Use `dvc status` when DVC is configured and inspect the actual dependency chain. If required evidence is stale, missing, or not reproducible from the recorded pipeline, do not present it as current or finalized. Report the affected stage and recommend reproduction first.

Maintain `.research/traceability/manuscript-evidence.md`, updating only claims touched by the current task. Use repository-relative paths and specific stages, parameters, rows, keys, line ranges, or figure panels where available. Never add an evidence entry without checking its source.


Update `manuscript/results.md` when requested and report unresolved evidence gaps separately.
