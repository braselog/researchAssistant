---
name: plan-week
description: Creates a realistic weekly plan from project aims, synchronized tasks, GitHub work, decisions, calendar constraints, and researcher preferences. Use for /plan_week or start-of-week planning.
---

# Plan the week

Read the researcher profile, project aims, phase checklist, latest review, `tasks.md`, open GitHub issues/PRs, unresolved decisions, and the calendar skill. For the planning range, run `bash .github/skills/calendar/scripts/calendar-wrapper.sh week --brief` or the appropriate custom range, then query free time with explicit work hours from `~/.researchAssistant/researcher_telos.md`.

Run a lightweight state reconciliation first. Do not plan duplicate, closed, blocked, or already-completed work. Ask about unavailable days or deadlines only when the calendar and project records do not answer them. Propose research blocks and the required manual `/wrap-up` and review reminders first; add all calendar events only after explicit approval using the calendar skill.

## Planning rules
- Choose one primary weekly outcome tied to an active aim.
- Prioritize blockers, deadlines, dependencies, and decision-making work.
- Link each substantial item to its GitHub issue or decision record.
- Put quick personal actions in `tasks.md`; do not copy the full GitHub backlog into it.
- Match deep work to known preferences and actual calendar availability.
- Include buffer and explicit non-goals.
- Pair implementation with validation and the required state/documentation update.
- Always include a `/wrap-up` block at the end of each planned work session or, when that would be excessive, at least at the end of each substantive research day.
- Include `/weekly-review` near the end of the working week and `/plan-week` at the start of the next planning cycle.
- Include `/monthly-review` and `/quarterly-review` only when the applicable period ends during the planned week or the review is overdue.
- Treat these as short manual assistant calls, not automated analyses. Schedule calendar reminders with titles such as `Review: /wrap-up` and `Review: /weekly-review`.

## Output
```markdown
# Weekly plan: [week]
## Primary outcome
## Must complete
## Should complete
## If time allows
## Explicitly deferred
## Calendar-aware allocation
## Assistant calls and review reminders
## Risks, decisions, and buffer
```

Before finalizing, verify that the plan contains the appropriate `/wrap-up`, weekly, monthly, and quarterly review reminders. Save to `.research/logs/weekly/YYYY-MM-DD-plan.md` when requested. See [original guidance](reference/original-guidance.md) for work-inventory and scheduling preferences.
