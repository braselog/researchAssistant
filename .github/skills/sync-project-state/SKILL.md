---
name: sync-project-state
description: Reconciles tasks.md, GitHub issues and PRs, meeting actions, decision records, activity logs, and repository evidence into one coherent project state. Use before planning/reviews or when tracking may have drifted.
---

# Synchronize project state

Treat each store according to its role:
- `tasks.md`: lightweight personal queue;
- GitHub issues/PRs: substantial repository work and review lifecycle;
- `.research/decisions/`: durable rationale and consequences;
- activity/meeting logs: historical evidence;
- weekly plans: temporary prioritization views, not task stores.

## Workflow
1. Read all relevant stores and recent git history.
2. Match items using explicit IDs, links, wording, affected files, and meeting sources.
3. Detect duplicates, orphaned actions, completed-but-open work, closed-but-unverified work, conflicting priorities/statuses, and unrecorded decisions.
4. Produce a proposed reconciliation plan before destructive or remote changes.
5. Apply approved local updates and use `manage-github-work` for approved remote changes.
6. Preserve history and links; do not silently merge semantically different work.

## Output
```markdown
## State summary
## Conflicts and orphaned items
## Proposed updates
- [ ] tasks.md: ...
- [ ] GH-N: ...
- [ ] DNNNN: ...
## Applied updates
## Unresolved
```

When no stable identifier exists, add one rather than relying on approximate title matching.
