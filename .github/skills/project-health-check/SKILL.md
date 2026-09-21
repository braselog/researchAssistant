---
name: project-health-check
description: Detects stale, inconsistent, or weakly tracked research work across code, workflows, outputs, manuscript, tasks, decisions, and GitHub. Use proactively before reviews, releases, or when results may be out of sync.
---

# Check project health

Inspect repository state with deterministic evidence where possible.

## Check for
- code, configuration, or parameters newer than dependent outputs;
- DVC/workflow stages with missing dependencies, parameters, or stale outputs;
- methods inconsistent with scripts/configuration;
- results values or figure annotations unsupported by current outputs;
- manuscript claims whose `.research/traceability/manuscript-evidence.md` entry is missing, stale, or points to non-current pipeline outputs;
- figures missing captions or manuscript references;
- meeting actions not represented in tasks/issues;
- GitHub issues closed without acceptance evidence, or merged PRs leaving work open;
- active decisions not reflected in implementation, and superseded decisions still referenced;
- placeholders, skipped checks, silent fallbacks, or failing CI/tests;
- high-priority work with unresolved blockers.

Use file timestamps only as a clue, not proof. Prefer hashes, workflow status, diffs, test outputs, and explicit links.

## Output
Rank findings as critical, important, or informational. For each give evidence, impact, and the smallest corrective action. Route tracking inconsistencies to `sync-project-state`; code validity concerns to `verify-implementation` or `review-script`. Do not modify files unless asked.
