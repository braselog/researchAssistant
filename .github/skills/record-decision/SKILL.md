---
name: record-decision
description: Creates and maintains concise research decision records linked to aims, evidence, code, tasks, and GitHub work. Use when a consequential scientific, analytical, or project choice is made or reconsidered.
---

# Record a research decision

Use for choices whose rationale should survive the current session, especially choices affecting scientific interpretation, data inclusion, analysis design, algorithms, parameters, scope, or deliverables.

## Workflow
1. Check `.research/decisions/decision-index.md` for duplicates or superseded records.
2. Gather the decision, context, alternatives, evidence, rationale, consequences, and reconsideration condition. Do not invent missing rationale.
3. Create `.research/decisions/DNNNN-short-title.md` and add it to the index.
4. Link related aims, files, analyses, tasks, GitHub issues/PRs, meetings, and outputs.
5. If replacing a prior decision, mark the old record `Superseded` and cross-link both records. Never erase the history.

## Record format
```markdown
# DNNNN: [Decision]
**Status:** Proposed | Active | Superseded | Reversed
**Date:** YYYY-MM-DD
**Owners:** [stated owners]
**Related:** [AIM-N, GH-N, files, meeting]

## Context
## Decision
## Rationale and evidence
## Alternatives considered
## Consequences
## Reconsider if
```

A statement in notes or a meeting is a candidate until clearly agreed. Ask before formalizing ambiguity.
