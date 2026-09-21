---
name: task
description: Captures a lightweight todo in tasks.md and links substantial repository work to GitHub tracking. Use for /task, todos, assigned actions, or quick task capture.
---

# Capture a task

Parse optional `!high` or `!low`, then append the unchanged text as an unchecked item under `High Priority`, `Normal Priority`, or `Low Priority / Someday` in `tasks.md`. Confirm in one line. Do not deduplicate a direct user entry.

## Tracking rule
`tasks.md` is the personal action queue. Recommend a GitHub issue when work:
- spans sessions or multiple steps;
- changes repository code, analyses, data products, or manuscript outputs;
- needs review, discussion, acceptance criteria, or provenance; or
- may change scientific direction.

Preserve stable source references such as `[source: meeting:YYYY-MM-DD-slug]` when supplied by a meeting workflow.

Do not use a fixed time threshold. If an issue already exists, link the task as `[GH-42]` rather than creating a duplicate. Use `manage-github-work` when the user wants the issue created.
