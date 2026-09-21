---
name: wrap-up
description: Performs an end-of-day reconciliation of conversations, repository activity, tasks, decisions, GitHub work, and documentation. Use for /wrap_up at the end of the research day or before an extended break.
---

# End-of-day wrap-up

Use this as the daily consolidation point. It should preserve meaningful project context without turning every conversation or tool action into permanent documentation.

## Gather evidence

Read as relevant:

- today's files in `.research/context/daily/`;
- today's entry in `.research/logs/activity.md`;
- `git status --short`, `git diff --stat`, and today's commits;
- changed scripts, configuration, DVC files, analyses, results, figures, manuscript files, and documentation;
- `tasks.md`;
- related GitHub issues and pull requests;
- active records in `.research/decisions/`;
- today's meeting transcripts and summaries.

Treat daily context entries as candidates, not authoritative project state.

## Reconcile the daily context inbox

For each candidate entry:

1. Compare it with later conversation, repository evidence, tool outcomes, and existing project records.
2. Discard routine discussion, duplicates, rejected suggestions, and superseded interpretations.
3. Preserve the final accepted interpretation when later conversation corrects an earlier statement.
4. Verify claims about completed work against repository or tool evidence.
5. Ask only when ambiguity could materially change the durable record.

Do not turn an agent suggestion into a task unless the user accepted it or it follows directly from verified incomplete work.

## Route durable information

- Lightweight personal action -> `tasks.md`
- Substantial repository or multi-session work -> GitHub issue
- Consequential scientific, analytical, or technical choice -> `.research/decisions/`
- Verified completed work -> `.research/logs/activity.md`
- Unresolved but durable project context -> an appropriate project note
- Implemented setup or structural change -> README or project documentation

Preserve stable meeting source IDs and links to relevant aims, issues, decisions, files, outputs, and transcript paths. Do not create or materially update remote GitHub items without explicit approval.

## Reconcile repository state

1. Identify which tasks, issues, aims, and decisions today's changes addressed.
2. Distinguish work attempted, implemented, tested, and scientifically verified.
3. Propose closing or updating work only when its intended behaviour or acceptance criteria were checked.
4. Identify consequential choices that need decision records.
5. Flag code or parameter changes that may have made DVC outputs, methods, results, figures, captions, or `.research/traceability/manuscript-evidence.md` stale.
6. Preserve unresolved questions and identify the first useful next action.

## Draft the activity entry

Use this compact structure:

```markdown
## YYYY-MM-DD

**Session focus**: [one sentence]

**Accomplished**:
- [verified outcome]

**Decisions made**:
- [DNNNN] [decision and rationale, if applicable]

**Tracking updates**:
- [task/GH-N] [status or proposed update]

**Next steps**:
- [small actionable next step]

**Notes**:
- [unresolved observation or question]
```

Preserve useful notes already recorded today and avoid duplicate entries. Do not infer accomplishments, time spent, productivity, or motivation from timestamps or commit counts.

## Apply and archive

1. Present proposed GitHub changes or ambiguous durable records for approval.
2. Apply approved local updates.
3. Append or update today's activity entry.
4. Move each processed daily inbox file to `.research/context/archive/`.
5. Include the processing time in the archive filename so a second `/wrap_up` on the same date cannot overwrite it:

   `.research/context/archive/YYYY-MM-DD-HHMM.jsonl`

6. Do not delete archived context automatically.
7. If some candidates remain unresolved, copy only those entries into a new daily file and mark them clearly as unresolved.

## Final response

Report briefly:

- **Logged:** durable activity and decisions recorded
- **Tracking:** tasks or GitHub updates applied or awaiting approval
- **Staleness:** outputs or documentation that may need regeneration
- **Unresolved:** context carried forward
- **Next:** the first recommended action

Do not add a full narrative when nothing substantial occurred.
