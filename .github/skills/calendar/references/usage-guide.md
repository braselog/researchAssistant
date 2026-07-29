# Calendar Integration - Usage Guide

## Overview

This skill provides access to Apple Calendar via icalBuddy. It can read from **all** calendars in Apple Calendar, including:
- iCloud calendars
- **Exchange/Outlook calendars** (e.g., Manchester)
- Google Calendar subscriptions
- Other calendar sources

**Supports both local and remote access** - work from a remote server but access your local Mac's calendar via SSH.

## Architecture

```
User/RA
  ↓
calendar-wrapper.sh (routes based on .env)
  ↓
  ├─ LOCAL MODE  → calendar-cli.sh → icalBuddy → Apple Calendar
  └─ REMOTE MODE → ssh local-pc → calendar-cli.sh → icalBuddy → Apple Calendar
```

The wrapper transparently routes commands to local or remote execution.

## Prerequisites

- macOS with Calendar.app
- `icalBuddy` installed: `brew install ical-buddy`
- Calendars set up in Apple Calendar

## Remote Access Setup

If you're working from a remote server but want to access your local Mac's calendar:

**1. Run the automated setup:**
```bash
bash .github/skills/calendar/scripts/setup-ssh.sh
```

This will:
- Generate SSH keys
- Ask for your local machine's IP and username
- Automatically copy the key (you enter password once)
- Configure SSH alias (`local-pc`)
- Test connection
- Update `.env` automatically

**2. Configuration in `.env`:**
```env
# Local mode (default)
CALENDAR_PROJECT_LOCATION=local

# Remote mode (after setup)
CALENDAR_PROJECT_LOCATION=remote
CALENDAR_LOCAL_SSH_HOST=local-pc
CALENDAR_LOCAL_SSH_USER=yourusername
CALENDAR_LOCAL_IP=192.168.1.100
CALENDAR_CLI_PATH=/path/to/calendar-cli.sh
```

**3. Switch modes:**
Just change `CALENDAR_PROJECT_LOCATION` in `.env` - all commands remain identical.

## Calendar Filtering

Set which calendars to query by default in your `.env` file:

```bash
# Comma-separated list, no spaces
DEFAULT_CALENDARS=Manchester,Family,Church
```

## Command Reference

### List Calendars

```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh calendars
```

### View Events

```bash
# Today's events
bash .github/skills/calendar/scripts/calendar-wrapper.sh today

# This week's events (Monday-Sunday)
bash .github/skills/calendar/scripts/calendar-wrapper.sh week

# Next week's events
bash .github/skills/calendar/scripts/calendar-wrapper.sh next-week

# Custom date range
bash .github/skills/calendar/scripts/calendar-wrapper.sh list --from 2026-01-10 --to 2026-01-17

# Filter by specific calendar
bash .github/skills/calendar/scripts/calendar-wrapper.sh list --from 2026-01-10 --to 2026-01-17 --calendar "Manchester"

# Brief output (hide notes, attendees, URLs) - recommended for AI
bash .github/skills/calendar/scripts/calendar-wrapper.sh today --brief
```

### Add Events

```bash
# Basic meeting
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Team Standup" \
  --date 2026-01-10 \
  --start 09:00 \
  --end 09:30

# With calendar and location
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Client Meeting" \
  --date 2026-01-10 \
  --start 14:00 \
  --end 15:00 \
  --calendar "Manchester" \
  --location "Zoom"

# Block focus time
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Focus: Deep Work" \
  --date 2026-01-10 \
  --start 09:00 \
  --end 12:00

# All-day event
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Vacation" \
  --date 2026-01-25 \
  --all-day
```

### Check Free Time

```bash
# Free slots today (uses work hours from researcher_telos.md)
bash .github/skills/calendar/scripts/calendar-wrapper.sh free

# Free slots on a specific day
bash .github/skills/calendar/scripts/calendar-wrapper.sh free --date 2026-01-10

# Custom working hours (override telos settings)
bash .github/skills/calendar/scripts/calendar-wrapper.sh free \
  --date 2026-01-10 \
  --work-start 08:00 \
  --work-end 17:00
```

## AI Assistant Integration

**Key principle:** Use `--brief` flag to reduce context size.

### Typical Workflow

```bash
# 1. See what's scheduled
bash .github/skills/calendar/scripts/calendar-wrapper.sh week --brief

# 2. Check free time for a specific day
bash .github/skills/calendar/scripts/calendar-wrapper.sh free --date 2026-01-10

# 3. Block focus time
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Focus: [Task from tasks.md]" \
  --date 2026-01-10 \
  --start 09:00 \
  --end 12:00
```

### Event Title Conventions

- `Focus:` - Deep work/coding time
- `Meeting:` - Meetings with others
- `Review:` - Review sessions
- `Planning:` - Planning sessions
- `Admin:` - Administrative tasks

## Using from Python

The wrapper automatically handles local vs remote routing:

```python
import subprocess

def run_calendar_command(args):
    """Run calendar command via wrapper (handles local/remote automatically)"""
    cmd = ['bash', '.github/skills/calendar/scripts/calendar-wrapper.sh'] + args
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout

# Usage examples
events = run_calendar_command(['week', '--brief'])
print(events)

free_slots = run_calendar_command(['free', '--date', '2026-01-10'])
print(free_slots)

# Add event
run_calendar_command([
    'add',
    '--title', 'Focus: Analysis',
    '--date', '2026-01-10',
    '--start', '09:00',
    '--end', '12:00'
])
```

## Output Format

### Event Listing

```
• Logan-Magnus (Manchester)
    14:00 - 15:00
• End Work (Office) (Family)
    15:30
```

### Free Slots

```
FREE TIME SLOTS:
----------------------------------------
  09:00 - 11:30  (2h 30m)
  14:00 - 15:30  (1h 30m)

SCHEDULED EVENTS:
----------------------------------------
  11:30 - 14:00  Team Meeting
  15:30 - 17:00  Client Call
```

## Troubleshooting

### Terminal windows appearing
This is expected - the CLI uses Terminal.app to run icalBuddy (permissions workaround). Windows close automatically.

### Events not appearing
Check that the calendar is in the `DEFAULT_CALENDARS` list in `.env` (comma-separated, no spaces).

List all available calendars:
```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh calendars
```

### Cannot connect to local-pc (remote mode)
1. Verify local Mac is powered on and network-accessible
2. Check Remote Login is enabled: System Settings > General > Sharing > Remote Login
3. Test connection: `ssh local-pc "echo test"`
4. Re-run setup: `bash .github/skills/calendar/scripts/setup-ssh.sh`

### Time format
Always use 24-hour format: `14:00` not `2:00 PM`  
Always use ISO dates: `2026-01-10` not `January 10, 2026`

### icalBuddy not installed
```bash
brew install ical-buddy
```

## Architecture Details

### Local Mode (Default)
```
wrapper → calendar-cli.sh → icalBuddy → Apple Calendar
```
Commands run directly on the current machine.

### Remote Mode
```
wrapper → ssh local-pc → calendar-cli.sh → icalBuddy → Apple Calendar
```
Commands execute on your local Mac via SSH. The wrapper reads `.env` and routes transparently.

### Why icalBuddy?

This skill previously used CalDAV, which couldn't access Exchange/Outlook calendars added to Apple Calendar. The current icalBuddy approach reads from Apple Calendar's local database, so it sees **all** calendars regardless of source (iCloud, Exchange, Google, etc.).

**Key files:**
- `calendar-wrapper.sh` - Routes commands (local vs remote)
- `calendar-cli.sh` - Backend that calls icalBuddy
- `setup-ssh.sh` - One-time remote access setup
