### name: plan-week
description: Creates a calendar-aware weekly priority framework from current work, fixed commitments, dependencies, and researcher preferences. Use for /plan_week or start-of-week planning.

## Plan the week

Create a flexible priority framework, not a detailed prediction of how research will unfold.

### Minimum context

Read only:
- the latest weekly review;
- current open GitHub issues and lightweight tasks;
- known deadlines, meetings, and preparation needs;
- calendar availability;
- unresolved blockers that affect work ordering.

Consult project telos, decisions, or repository details only when needed to resolve ambiguity. Invoke `sync-project-state` only when a concrete inconsistency would materially affect the plan.

### Planning rules

- Choose one primary weekly outcome tied to an active aim.
- Separate fixed commitments from flexible project work.
- Schedule meetings, preparation, follow-up, deadlines, reviews, and planning precisely.
- Represent project work as an ordered queue: start item, next item, fallback if blocked, and explicitly deferred work.
- Link substantial items to their GitHub issue or decision record. Do not copy full issue scope or acceptance criteria into the plan.
- Do not infer duration from an issue title, issue length, or apparent complexity.
- Use an effort estimate only when supported by prior work, a concrete breakdown, comparable evidence, or a user estimate.
- When effort is uncertain, schedule an initial investigation block and a checkpoint. Do not allocate the remainder of the week by default.
- Prescribe issue internals only when dependencies, next steps, and acceptance criteria are already understood or the user requests detailed implementation planning.
- Use flexible focus blocks such as `Highest-priority unblocked issue` when exact work cannot be predicted.
- Include buffer and explicit non-goals.
- Include `/wrap-up` after substantive research days, `/weekly-review` near the end of the week, and `/plan-week` at the next planning point. Include monthly or quarterly reminders only when due.
- Propose calendar events first. Add them only after explicit approval through the calendar skill.

### Replanning triggers

Reassess the queue when:
- the current issue is completed;
- it becomes materially blocked;
- a meeting changes priorities;
- new evidence invalidates a dependency; or
- the primary weekly outcome is achieved early.

Use `/next` to select the immediate next issue. Regenerate the weekly plan only when the weekly outcome, capacity, constraints, or priority order materially changes.

### Output

# Weekly plan: [week]
## Primary outcome
## Fixed commitments and preparation
## Ordered work queue
## Dependencies and fallback work
## Explicitly deferred
## Flexible focus blocks
## Wrap-up and review reminders
## Replanning triggers

### Persist the result

The Markdown file is the authoritative output. Write the final plan automatically to:

`.research/logs/weekly/YYYY-MM-DD-plan.md`

Create the directory if needed. Then show only a concise summary and saved path in chat.
