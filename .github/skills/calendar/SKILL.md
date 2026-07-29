---
name: calendar
description: View calendar schedule, check availability, find free time slots, and block time for research tasks. Works with all calendars in Apple Calendar including Exchange/Outlook. Use when user asks about their schedule, availability, or wants to add calendar events.
---

# Calendar Integration

Access Apple Calendar via icalBuddy to manage schedule, find availability, and block time for research work.

## When to Use

Invoke this skill when the user:
- Asks to see their schedule ("What's on my calendar today?", "Show me this week")
- Wants to check availability ("When am I free tomorrow?", "Do I have any 2-hour blocks?")
- Requests time blocking ("Block 9-11am tomorrow for analysis")
- Asks about specific events ("When is my next meeting?")
- Wants to add calendar events for research tasks
- Needs help planning their day/week based on availability

## How It Works

This skill uses `icalBuddy` via a bash script to access Apple Calendar. It can read from **all** calendar sources:
- iCloud calendars
- **Exchange/Outlook calendars** (e.g., work calendars added to Apple Calendar)
- Google Calendar subscriptions
- Any calendar visible in Apple Calendar

The script uses Terminal.app as a workaround for permissions - brief Terminal windows may appear and close automatically.

## Prerequisites

**Required:**
- macOS with Calendar.app
- `icalBuddy` installed
- Calendars configured in Apple Calendar

**Install icalBuddy (if needed):**
```bash
brew install ical-buddy
```

**Configuration:**
Calendar filtering is configured in `.env`:

```bash
DEFAULT_CALENDARS=Manchester,Family,Church
DEFAULT_WRITE_CALENDAR=Manchester
CALENDAR_PROJECT_LOCATION=local  # or 'remote' for remote access
```

**First-time setup (recommended):**

```bash
python3 .github/skills/calendar/scripts/init_config.py
```
This will list all available calendars, let you choose which to read and which to write to, then update `.env` automatically.

Edit the `DEFAULT_CALENDARS` line in your `.env` file to match the calendars you want to query by default (comma-separated, no spaces).

**For Remote Access:**
If you're working from a remote server but want to access your local machine's calendar, see the "Remote Access Setup" section below.

## Execution Steps

**Important: All commands below should be run through the wrapper script:**

```bash
# Use calendar-wrapper.sh instead of calendar-cli.sh directly
bash .github/skills/calendar/scripts/calendar-wrapper.sh <command> [options]
```

The wrapper automatically routes commands to local or remote execution based on `.env` configuration.

### 1. Check Today's Schedule

```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh today --brief
```

**What it does:** Shows events for today from configured calendars  
**Use `--brief`:** Hides notes/attendees/URLs (recommended for AI to reduce context)

### 2. Check This Week's Schedule

```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh week --brief
```

**What it does:** Shows Monday-Sunday events from configured calendars

### 3. Find Free Time Slots

**MANDATORY WORKFLOW:**

**Step 1: Check work hours in researcher_telos.md**
- Read `~/.researchAssistant/researcher_telos.md` (use `cat` in terminal - outside workspace)
- Look for the "Work Preferences" section
- If work hours are NOT specified or are incomplete, proceed to Step 2
- If work hours ARE specified, use them and skip to Step 4

**Step 2: ASK THE USER (if work hours missing)**
- Ask: "What are your work hours? (e.g., 9:00-17:00, 8:00-18:00)"
- Wait for their response

**Step 3: UPDATE researcher_telos.md**
- Add or update the work hours in the "Work Preferences" section
- Example format:
  ```markdown
  ### Work Hours
  - **Daily work hours**: 08:00-18:00
  - **Preferred work blocks**: 1-hour blocks
  ```

**Step 4: Run the calendar command**
- Use the work hours (either existing or newly added) with the command:

```bash
# Specific date with work hours from researcher_telos.md
bash .github/skills/calendar/scripts/calendar-wrapper.sh free --date 2026-01-10 --work-start 08:00 --work-end 18:00

# Today with work hours from researcher_telos.md
bash .github/skills/calendar/scripts/calendar-wrapper.sh free --work-start 08:00 --work-end 18:00
```

**What it does:** Analyzes schedule and returns available time blocks with durations

**CRITICAL:** Never assume or use default work hours. Always verify with researcher_telos.md first (use `cat ~/.researchAssistant/researcher_telos.md` in terminal). If not specified, ask the user and update their profile.

### 4. Block Time for Research

```bash
# Basic time block
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Focus: Deep Work" \
  --date 2026-01-10 \
  --start 09:00 \
  --end 12:00

# With specific calendar
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Focus: Analysis Pipeline" \
  --date 2026-01-10 \
  --start 09:00 \
  --end 12:00 \
  --calendar "Manchester"

# With location
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Meeting: Lab Sync" \
  --date 2026-01-10 \
  --start 14:00 \
  --end 15:00 \
  --location "Zoom"

# All-day event
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Conference" \
  --date 2026-01-15 \
  --all-day
```

**Always confirm with user before adding events.**

### 5. List All Available Calendars

```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh calendars
```

**Use this to:** Help user identify which calendars they have, troubleshoot filtering

## Command Reference

| Action | Command |
|--------|---------|
| Today's events | `bash .github/skills/calendar/scripts/calendar-wrapper.sh today --brief` |
| This week | `bash .github/skills/calendar/scripts/calendar-wrapper.sh week --brief` |
| Next week | `bash .github/skills/calendar/scripts/calendar-wrapper.sh next-week --brief` |
| Custom range | `bash .github/skills/calendar/scripts/calendar-wrapper.sh list --from YYYY-MM-DD --to YYYY-MM-DD --brief` |
| Free time today | `bash .github/skills/calendar/scripts/calendar-wrapper.sh free` |
| Free time specific day | `bash .github/skills/calendar/scripts/calendar-wrapper.sh free --date YYYY-MM-DD` |
| List calendars | `bash .github/skills/calendar/scripts/calendar-wrapper.sh calendars` |

**Time format:** Use 24-hour format (14:00, not 2:00 PM)  
**Date format:** Use ISO format (2026-01-10, not January 10)

## Research Workflow Integration

### Weekly Planning

When user runs `/plan-week` or asks to plan their week:

1. **Check existing commitments:**
   ```bash
   bash .github/skills/calendar/scripts/calendar-wrapper.sh week --brief
   ```

2. **For each day needing work blocks:**
   ```bash
   bash .github/skills/calendar/scripts/calendar-wrapper.sh free --date YYYY-MM-DD
   ```

3. **Identify tasks from `tasks.md` and `.research/project_telos.md`**

4. **Propose time blocks matching task requirements and free slots**

5. **If approved, add to calendar:**
   ```bash
   bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
     --title "Focus: [Task from tasks.md]" \
     --date YYYY-MM-DD \
     --start HH:MM \
     --end HH:MM
   ```

### Time Blocking by Research Phase

Different phases benefit from different block sizes:

- **PLANNING**: 1-2 hour blocks (literature review, hypothesis)
- **DEVELOPMENT**: 2-4 hour blocks (pipeline building - minimize interruptions)
- **ANALYSIS**: 1-2 hour blocks (running experiments, checking outputs)
- **WRITING**: 2-3 hour blocks (manuscript drafting)

Consider user's productive hours from `~/.researchAssistant/researcher_telos.md` (use `cat` in terminal - outside workspace) when suggesting blocks.

### Event Title Conventions

Use consistent prefixes for clarity:
- `Focus:` - Deep work/coding time
- `Meeting:` - Meetings with others
- `Review:` - Code/document review
- `Planning:` - Planning sessions
- `Admin:` - Administrative tasks

Example: `Focus: DVC Pipeline - Aim 1 Analysis`

## Best Practices for AI Execution

1. **Validate work hours FIRST** - Before any free time query:
   - Check `~/.researchAssistant/researcher_telos.md` for work hours (use `cat` in terminal - outside workspace)
   - If NOT specified → Ask user → Update telos file → Then run command
   - If specified → Use those hours immediately
   - **NEVER use default hours without asking**

2. **Always use `--brief` flag** - Reduces context size by hiding notes/attendees/URLs
3. **Check free time before suggesting blocks** - Don't propose times that are busy
4. **Confirm before adding events** - Always ask user approval first
5. **Match titles to tasks.md** - Use consistent naming for tracking
6. **Block in 2-3 hour chunks** for deep work (research shows this is optimal)
7. **Leave 15-minute buffers** between meetings
8. **Update researcher_telos.md when info is missing** - This profile is source of truth for your preferences

## Output Interpretation

### Schedule Output

```
• Logan-Magnus (Manchester)
    14:00 - 15:00
• End Work (Office) (Family)
    15:30
```

Format: `• Title (Calendar)\n    time`

### Free Slots Output

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

Use the duration to match with task time requirements.

## Troubleshooting

### Terminal windows briefly appear
Expected behavior - the script uses Terminal.app for permissions. Windows close automatically.

### Events not showing up
1. Run: `bash .github/skills/calendar/scripts/calendar-wrapper.sh calendars`
2. Check if the calendar is in the `DEFAULT_CALENDARS` list in `.env`
3. Edit `.env` to include the missing calendar (comma-separated, no spaces)

### icalBuddy not found
```bash
brew install ical-buddy
```

### Wrong timezone
Events showing incorrect times? The script uses local system timezone automatically via Calendar.app.

### Remote connection issues
1. Verify local machine is powered on and network-accessible
2. Check SSH/Remote Login is enabled: System Settings > General > Sharing > Remote Login
3. Test connection: `ssh local-pc "echo 'test'"`
4. Re-run setup if needed: `bash .github/skills/calendar/scripts/setup-ssh.sh`

## Remote Access Setup

If you're working from a remote server (e.g., SSH into a Linux box) but want to access your local Mac's calendar, follow this setup.

### Overview

The calendar skill can operate in two modes:
- **Local**: Run calendar commands directly on this machine (default)
- **Remote**: Execute commands via SSH to your local Mac

### Quick Setup

**1. Run the automated setup script:**

```bash
bash .github/skills/calendar/scripts/setup-ssh.sh
```

This script will:
- ✓ Generate SSH keys (if not already present)
- ✓ Display your public key to copy
- ✓ Ask for your local machine's IP address and username
- ✓ Configure SSH connection alias (`local-pc`)
- ✓ **Automatically copy the key to your local machine** (you'll enter password once)
- ✓ Test the connection
- ✓ Update your `.env` file automatically

**2. During setup, you'll need to:**

- Enter your local machine's **password** when prompted (one time only)
- Ensure Remote Login is enabled on your local Mac (see below)

**3. Enable Remote Login on your local Mac:**

System Settings > General > Sharing > Remote Login (turn ON)

### Configuration

After running `setup-ssh.sh`, your `.env` will contain:

```env
# Local mode (default) - commands run on this machine
CALENDAR_PROJECT_LOCATION=local

# Remote mode - commands execute via SSH
CALENDAR_PROJECT_LOCATION=remote
CALENDAR_LOCAL_SSH_HOST=local-pc
CALENDAR_LOCAL_SSH_USER=yourusername
CALENDAR_LOCAL_IP=192.168.1.100
CALENDAR_CLI_PATH=/Users/yourusername/Documents/researchAssistant/.github/skills/calendar/scripts/calendar-cli.sh
```

### How It Works

When `CALENDAR_PROJECT_LOCATION=remote`:

1. You run: `bash calendar-wrapper.sh today`
2. Wrapper reads `.env` and sees "remote"
3. Wrapper executes via SSH: `ssh local-pc "bash /path/to/calendar-cli.sh today"`
4. Your local Mac runs the command and returns results
5. You see the output as if running locally

**All calendar commands remain the same** - the wrapper handles routing transparently.

### Switching Between Local and Remote

Edit `.env` to change modes:

```bash
# Use local calendar (current machine)
CALENDAR_PROJECT_LOCATION=local

# Use remote calendar (SSH to local Mac)
CALENDAR_PROJECT_LOCATION=remote
```

No other changes needed - all commands work identically.

### Manual SSH Setup (Advanced)

If you prefer to configure SSH manually or troubleshoot issues:

**1. Generate SSH key (if needed):**

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

**2. Copy public key to local machine:**

```bash
# Use ssh-copy-id (recommended)
ssh-copy-id -i ~/.ssh/id_rsa.pub yourusername@192.168.1.100

# Or manually via SSH
cat ~/.ssh/id_rsa.pub | ssh yourusername@192.168.1.100 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

You'll be prompted for your password on the local machine.

**3. Create SSH config:**

```bash
# On remote machine
nano ~/.ssh/config
```

Add:

```text
Host local-pc
    HostName 192.168.1.100  # Your local Mac's IP
    User yourusername       # Your username on local Mac
    IdentityFile ~/.ssh/id_rsa
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
```

Save and set permissions:

```bash
chmod 600 ~/.ssh/config
```

**4. Test connection:**

```bash
ssh local-pc "echo 'Connection successful'"
```

**5. Update `.env`:**

Add the calendar remote access section as shown in the "Configuration" section above.

### Security Notes

- SSH keys are stored in `~/.ssh/id_rsa` (keep private!)
- Connections use key-based authentication (no passwords)
- `StrictHostKeyChecking no` is used for convenience with dynamic IPs
- Only your user account on the local Mac can be accessed
- Calendar data never leaves your machines

### Requirements for Remote Access

**On the remote machine (where you're working):**
- SSH client installed (standard on Linux/macOS)
- Network access to your local machine
- This repository cloned

**On the local machine (Mac with Calendar.app):**
- macOS with Calendar.app
- `icalBuddy` installed (`brew install ical-buddy`)
- Remote Login enabled (System Settings > Sharing)
- This repository cloned at the path specified in `CALENDAR_CLI_PATH`
- Same calendars configured in Calendar.app

### Dynamic IP Addresses

If your local Mac's IP changes frequently:

**Option 1: Update .env**
```bash
# Update IP in .env
sed -i 's/CALENDAR_LOCAL_IP=.*/CALENDAR_LOCAL_IP=192.168.1.XXX/' .env
```

**Option 2: Use hostname (if on same network)**
```bash
# In .env, use .local hostname instead of IP
CALENDAR_LOCAL_IP=your-macbook-name.local
```

**Option 3: Set static IP on local Mac**
System Settings > Network > [Your Connection] > Details > TCP/IP > Configure IPv4: Manually

## Example Usage

### Scenario 1: Daily Planning

**User:** "What's on my schedule today?"

**Execute:**
```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh today --brief
```

**Respond with formatted output:**
```
📅 Thursday, January 9, 2026

• Logan-Magnus (Manchester)
    14:00 - 15:00
• End Work (Office) (Family)
    15:30

You have free time: Before 2pm and after 3:30pm.
```

### Scenario 2: Finding Deep Work Time

**User:** "I need 3 hours tomorrow to work on my analysis. When am I free?"

**Execute:**
```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh free --date 2026-01-10
```

**Interpret output and respond:**
```
Looking at Friday, January 10:

FREE TIME SLOTS:
  09:00 - 12:00  (3h 0m) ← Perfect fit!
  14:00 - 16:30  (2h 30m)

The morning block (9am-12pm) is ideal for deep work.
Should I block 9am-12pm for "Focus: Analysis Pipeline"?
```

**If approved:**
```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh add \
  --title "Focus: Analysis Pipeline" \
  --date 2026-01-10 \
  --start 09:00 \
  --end 12:00
```

### Scenario 3: Weekly Planning

**User:** "/plan-week" or "Help me plan this week"

**Execute:**
```bash
bash .github/skills/calendar/scripts/calendar-wrapper.sh week --brief
```

**Then for each work day:**
1. Check tasks from `tasks.md`
2. Check current phase from `.research/project_telos.md`
3. Find free slots for each day needing blocks
4. Propose specific time blocks matching tasks
5. Add approved blocks to calendar

## Notes

- This skill uses **model-invocation** - RA should recognize calendar requests automatically
- No explicit `/calendar` slash command needed
- Always confirm before adding events
- **Use the wrapper script** (`calendar-wrapper.sh`) not `calendar-cli.sh` directly
- The wrapper automatically routes to local or remote execution based on `.env`
- Calendar filtering is configured via `DEFAULT_CALENDARS` in `.env`
- The script sees ALL calendars in Apple Calendar, including Exchange/Outlook
- For remote access, run `setup-ssh.sh` once to configure passwordless authentication

## See Also

- `/plan-week` - Weekly planning that uses calendar integration
- `tasks.md` - Source of truth for what to schedule
- `.research/project_telos.md` - Current phase affects time blocking strategy
- `.github/skills/calendar/scripts/setup-ssh.sh` - Remote access setup script
