---
name: sync-tasks
description: Bidirectional mirror sync between tasks.md and GitHub Projects. Syncs task content, status (Backlog/Ready/In Progress/In Review/Done), and priority (P0/P1/P2).
---

# Sync Mobile Tasks (Mirror Sync)

## When to Use

- User explicitly runs `/sync-tasks` or `/sync-tasks github` or `/sync-tasks local`
- User mentions syncing tasks with mobile/phone
- User wants tasks accessible on GitHub mobile app
- User needs to sync status or priority changes between local and remote
- User specifies which source should take priority during conflicts

## What It Does

**True bidirectional mirror sync between tasks.md and GitHub Projects:**

- Maintains identical task state in both locations
- Syncs task content, status, and priority fields
- Tasks format: `- [ ] Task title - **Priority**`
- Sections match GitHub status: `## Backlog`, `## Ready`, `## In Progress`, `## In Review`, `## Done`
- Priorities: **P0** (highest), **P1**, **P2**

## Usage

### Sync Commands

**Bidirectional sync** (both sources can update each other):
```bash
python3 .github/skills/sync-tasks/scripts/sync_mobile.py
```

**GitHub priority** (changes you made on mobile override local):
```bash
python3 .github/skills/sync-tasks/scripts/sync_mobile.py github
```

**Local priority** (your local changes override GitHub):
```bash
python3 .github/skills/sync-tasks/scripts/sync_mobile.py local
```

### Priority Modes Explained

| Mode | When to Use | What Happens |
|------|-------------|-------------|
| **github** | You edited tasks on mobile and want to pull those changes | GitHub status/priority overwrite tasks.md for existing tasks |
| **local** | You edited tasks.md locally and want to push those changes | tasks.md status/priority overwrite GitHub for existing tasks |
| **(none)** | Regular sync, both sources can update | Last write wins, bidirectional updates |

### Workflow

1. **Edit locally** - Add/update tasks in [tasks.md](tasks.md):
   ```markdown
   ## Ready
   - [ ] Review paper on methods - **P0**
   - [ ] Fix preprocessing bug - **P1**
   
   ## In Progress
   - [ ] Run analysis on new data - **P0**
   ```

2. **Run sync** - Execute `/sync-tasks` or run the script

3. **View on mobile** - Open GitHub mobile app → Your Project → See all tasks with status/priority

4. **Edit on mobile** - Change status, priority, or add new tasks

5. **Sync again** - Changes from mobile appear in tasks.md

## Configuration

### First-Time Setup

Before running the sync for the first time, you must initialize the configuration:

```bash
python3 .github/skills/sync-tasks/scripts/init_config.py
```

This script will:
1. **Prompt for missing values** in [.env](.env):
   - `GITHUB_ORG_NAME`: Your GitHub organization name
   - `GITHUB_PROJECT_NUM`: Your project board number
   - `GITHUB_TASKS_FILE`: Local file to sync (default: tasks.md)

2. **Auto-discover project configuration** using `gh` CLI:
   - Project ID
   - Status and Priority field IDs
   - All option IDs for status values (Backlog, Ready, In progress, In review, Done)
   - All option IDs for priority values (P0, P1, P2)

3. **Generate [gh.yaml](.github/skills/sync-tasks/gh.yaml)** with discovered values

**Note**: This only needs to be run once. The configuration is saved in [.env](.env) and [gh.yaml](.github/skills/sync-tasks/gh.yaml).

### Reconfiguration

To reconfigure (e.g., switch to a different project):
```bash
# Remove the generated config
rm .github/skills/sync-tasks/gh.yaml

# Run init again
python3 .github/skills/sync-tasks/scripts/init_config.py
```

## Execution Steps

1. **Determine priority mode** from user request:
   - If user says "github" or mentions mobile changes → use `github` mode
   - If user says "local" or mentions local changes → use `local` mode
   - If no preference specified → use bidirectional (no argument)

2. **Run the appropriate command:**
   ```bash
   # Navigate to project root
   cd /Users/user/Documents/researchAssistant
   
   # Run sync with appropriate mode
   python3 .github/skills/sync-tasks/scripts/sync_mobile.py [github|local]
   ```

3. **Confirm results** and report to user what was synced

## Implementation Status

✅ **Fully implemented** - Priority modes working
- ✅ Bidirectional sync (default)
- ✅ GitHub priority mode
- ✅ Local priority mode
- ✅ Task content, status, and priority sync

## Tips

- **P0** = High priority (urgent)
- **P1** = Normal priority
- **P2** = Low priority
- Keep tasks under 2 hours (create GitHub Issues for larger work)
- Checked tasks `[x]` auto-move to Done section on sync
- The sync is designed to be idempotent - safe to run multiple times
