### name: monthly-review
description: Reviews monthly progress against aims using weekly reviews and material project evidence. Use for /monthly_review, milestones, or PI reporting.

## Monthly project review

Use weekly reviews as the primary input. Consult decisions, issues, repository state, deliverables, and manuscript evidence only where needed to verify material claims or resolve inconsistency. Do not reconstruct the month from every project store when weekly reviews are current.

Assess progress by aim, changes in direction, repeated blockers, validation and reproducibility status, deliverable readiness, and material tracking drift. Do not use arbitrary completion percentages, activity counts, or unsupported duration estimates.

### Output

# Monthly review: [month]
## Executive summary
## Progress and evidence by aim
## Decisions and changes in direction
## Tracking and repository consistency
## Risks and unresolved validity questions
## Deliverable status
## Next-month priorities

### Persist the result

Write the authoritative review automatically to:

`.research/logs/monthly/YYYY-MM.md`

Create the directory if needed. Then show only a concise summary and saved path in chat.
