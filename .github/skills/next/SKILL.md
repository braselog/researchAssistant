---
name: next
description: Assesses repository, task, decision, GitHub, meeting, calendar, and unprocessed context state to recommend the highest-value next actions. Use for /next, session starts, uncertainty about priorities, or after completing work.
---

# Recommend the next action

## Read relevant project state

Consult only what is needed:

- `~/.researchAssistant/researcher_telos.md`
- `.research/project_telos.md`
- `.research/phase_checklist.md`
- recent entries in `.research/logs/activity.md`
- `tasks.md`
- active records in `.research/decisions/`
- open GitHub issues and pull requests
- git status and recent commits
- the calendar when scheduling affects feasibility

Treat phases as guidance, not rigid gates.

## Check unprocessed context first

Inspect `.research/context/daily/` for daily context files.

- If a file exists from a previous date, flag it before planning:

  `Unprocessed project context remains from YYYY-MM-DD. Run /wrap_up to reconcile it before relying on the current task and decision state.`

- Do not process or archive the inbox during `/next`.
- A file for the current date is expected during an active workday and should not block recommendations.
- If stale context materially affects confidence, state which recommendations are provisional.

## Assess project state

Look for material conditions such as:

- unprocessed meeting actions or candidate decisions;
- local tasks duplicated by, missing from, or inconsistent with GitHub issues;
- completed repository work still marked open;
- closed work whose acceptance criteria were not verified;
- decisions not reflected in code, analysis, or documentation;
- stale DVC outputs or downstream artifacts after code or parameter changes;
- drift among code, methods, results, figures, captions, and the manuscript evidence map;
- failed checks, unresolved blockers, and important deadlines;
- new data, meeting audio, figures, or manuscript gaps relevant to an active aim;
- overdue wrap-ups or weekly, monthly, or quarterly reviews.

Use `sync-project-state` or `project-health-check` when inconsistency is material. Raise only issues that could change the recommended next action.

## Priority order

1. Correctness, blocked work, and unresolved scientific decisions
2. Hard deadlines and dependencies
3. The active aim's highest-value work
4. Stale tracking, reproducibility, or documentation risks
5. Routine planning and maintenance

When scheduling or near-term feasibility matters, use the `calendar` skill to read the relevant range with `--brief`. Do not query the calendar for purely technical prioritization questions.

## Output

Provide a concise context summary and at most three options:

```markdown
**Context:** [current aim/phase, recent progress, and any material warning]

A) **[Highest-value action]**
   [Why it matters and the concrete file, issue, decision, skill, or command]

B) **[Second action]**
   [Why]

C) **[Optional maintenance action]**
   [Why]
```

Mention uncertainty rather than pretending project state is fully synchronized. Do not print the full skill registry.
