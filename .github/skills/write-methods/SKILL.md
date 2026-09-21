---
name: write-methods
description: Drafts or updates methods from actual code, configuration, DVC stages, environments, decisions, and provenance. Use for /write_methods or when methods may be out of sync with implementation.
---

# Write methods from implementation

Read the relevant scripts, tests, `dvc.yaml`, `dvc.lock`, `params.yaml`, environment specification, project aims, decision records, provenance, and existing methods.

Map each reported method to implemented and verified behaviour. Include details needed to reproduce the work: design, data sources, sample definitions, preprocessing, exclusions, algorithms, parameters, software versions, validation, statistics, and deviations from plans. Explain rationale only when documented; do not infer it from code.

Flag undocumented behaviour, unused parameters, hidden defaults, stale stages, and discrepancies between code and prose. Do not turn a code walkthrough into manuscript text or invent versions, sample sizes, thresholds, or validation.


## Reproducibility gate and evidence map
Before editing manuscript text, determine whether relevant DVC stages and source outputs are current. Use `dvc status` when DVC is configured and inspect the actual dependency chain. If required evidence is stale, missing, or not reproducible from the recorded pipeline, do not present it as current or finalized. Report the affected stage and recommend reproduction first.

Maintain `.research/traceability/manuscript-evidence.md`, updating only claims touched by the current task. Use repository-relative paths and specific stages, parameters, rows, keys, line ranges, or figure panels where available. Never add an evidence entry without checking its source.


Update `manuscript/methods.md` when requested and report unresolved gaps separately.
