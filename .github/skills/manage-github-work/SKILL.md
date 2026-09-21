---
name: manage-github-work
description: Creates and maintains research-aware GitHub issues and pull-request context using repository evidence. Use when work spans sessions, changes the repo, needs review, or must be linked to aims and decisions.
---

# Manage GitHub work

Use `gh` CLI when authenticated; otherwise produce the exact proposed issue or PR update and state that it was not applied.

## Create an issue when work
- spans sessions or multiple steps;
- changes code, analyses, outputs, or manuscript artifacts;
- needs review, acceptance criteria, discussion, or provenance; or
- implements a recorded decision.

Keep quick personal actions in `tasks.md`. Search open and closed issues before creating one.

## Issue content
```markdown
## Why
[Research or project context]
## Scope
- [work]
## Acceptance criteria
- [observable result or validation]
## Links
- Aim:
- Decision:
- Source meeting/task:
- Affected files/outputs:
```

Update issues when evidence changes, not merely because code was edited. Close only when acceptance criteria are satisfied. Link PRs to their issue and summarize scientific impact, validation, changed outputs, and remaining uncertainty. Never create, close, or materially rewrite remote items without explicit user intent.
