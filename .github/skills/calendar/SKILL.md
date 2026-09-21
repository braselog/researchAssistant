---
name: calendar
description: Views Apple Calendar schedules, checks availability, finds free time, and adds approved research blocks through the bundled icalBuddy wrapper. Use for calendar, schedule, availability, meeting, deadline, focus-time, or calendar-aware planning requests, including Exchange/Outlook calendars exposed through Apple Calendar.
---

# Calendar integration

Use the bundled wrapper to access Apple Calendar locally or through the configured SSH route. The wrapper supports iCloud, Exchange/Outlook, Google, and other calendars visible in Calendar.app.

## Required command path

Always execute:

```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh <command> [options]
```

Do not call `calendar-cli.sh` directly. The wrapper reads `.env` and routes local or remote execution.

## Common commands

```bash
# Compact schedule output
bash .github/skills/calendar/scripts/calendar-wrapper.sh today --brief
bash .github/skills/calendar/scripts/calendar-wrapper.sh week --brief
bash .github/skills/calendar/scripts/calendar-wrapper.sh next-week --brief
bash .github/skills/calendar/scripts/calendar-wrapper.sh list --from YYYY-MM-DD --to YYYY-MM-DD --brief

# Available calendars
bash .github/skills/calendar/scripts/calendar-wrapper.sh calendars

# Availability
bash .github/skills/calendar/scripts/calendar-wrapper.sh free --date YYYY-MM-DD --work-start HH:MM --work-end HH:MM

# Add an approved block
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Focus: [task]" --date YYYY-MM-DD --start HH:MM --end HH:MM
```

Prefer `--brief` for reads to avoid loading notes, attendees, and URLs.

## Availability workflow

1. Read `~/.researchAssistant/researcher_telos.md` for work hours and productive-time preferences.
2. If work hours are missing or incomplete, ask the user and offer to update the profile. Never silently use the CLI defaults.
3. Query the calendar for the relevant date range.
4. Run `free` with explicit `--work-start` and `--work-end` values.
5. Match proposed blocks to task type, duration, priority, dependencies, and the user's productive hours.
6. Leave sensible transition buffers around meetings when feasible; do not enforce a universal buffer or block length.

## Planning integration

For `plan-week`:
1. Run `week --brief` or a custom range.
2. Reconcile candidate work from `tasks.md`, open GitHub issues, active decisions, and project aims.
3. Query free time only for days that need allocation.
4. Propose specific blocks, but do not add them yet.
5. After approval, add each block using a title linked to the tracked work, for example `Focus: GH-42 - Validate donor split`.

For assistant workflow reminders, use concise event titles:
- `Review: /wrap-up`
- `Review: /weekly-review`
- `Review: /monthly-review`
- `Review: /quarterly-review`
- `Planning: /plan-week`

These events remind the user to invoke the skill manually; they do not execute skills automatically.

Calendar events constrain plans but are not task records. Preparation and follow-up work belongs in `tasks.md` or GitHub. Record only minimal calendar details in repository logs.

## Write safety

- Reading schedules and availability does not require confirmation.
- Always show the exact title, date, start/end time, and target calendar before adding an event.
- Add, move, invite, cancel, or edit events only after explicit approval.
- Use 24-hour times and ISO dates in commands.
- Preserve time zones and distinguish tentative events.

## Configuration and failures

First-time setup:

```bash
python3 .github/skills/calendar/scripts/init_config.py
```

The skill requires macOS Calendar.app and `icalBuddy`. Calendar filters, write calendar, and local/remote mode are configured in `.env`. If a command fails, report the actionable error rather than inferring an empty schedule.

For setup, remote access, troubleshooting, output examples, and the full command reference, read [usage-guide.md](references/usage-guide.md). 
