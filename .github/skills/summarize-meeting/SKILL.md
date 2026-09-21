---
name: summarize-meeting
description: Extracts decisions, actions, open questions, and insights from a meeting and routes trackable work into tasks.md, GitHub, or decision records. Use for /summarize_meeting or after transcription.
---

# Summarize a meeting

Read the transcript, `.research/project_telos.md`, `tasks.md`, recent decision records, and open GitHub issues when available.

## Extract precisely
- **Decision**: explicitly agreed choice, with rationale and conditions if stated.
- **Action**: explicit work item; preserve owner and deadline only when stated.
- **Proposal**: discussed but not adopted.
- **Open question**: unresolved uncertainty.
- **Insight**: context worth retaining but not yet actionable.

Do not infer agreement, ownership, deadlines, or speaker identity.

## Stable source reference
Create one stable source ID for the meeting using its date and a short slug, for example `meeting:2026-09-21-lab-sync`. Use the transcript path when available as the canonical link. Add this source to every routed item:

```markdown
- [ ] Prepare donor-level sensitivity analysis [source: meeting:2026-09-21-lab-sync]
```

GitHub issues and decision records should include the same source ID and transcript path. Preserve an existing meeting ID rather than creating a second one.

## Route without duplication
- Quick personal action -> propose/add to `tasks.md`.
- Repository or multi-session work -> propose/link a GitHub issue using `manage-github-work`.
- Consequential scientific or technical choice -> propose a decision record using `record-decision`.
- Already tracked -> add source links or context rather than duplicate it.

Ask before creating GitHub issues or formal decision records unless the user explicitly requested automatic updates.

## Summary structure
```markdown
# Meeting summary: [title/date]
## Decisions
## Actions
- [ ] [action] | Owner: [stated/unspecified] | Due: [stated/unspecified] | Tracking: [local/GH-N] | Source: [meeting ID]
## Proposals and insights
## Open questions
## State updates proposed
```
