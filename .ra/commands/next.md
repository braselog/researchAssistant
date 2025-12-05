# /next Command

> The catch-all command for researchers at any stage. Assesses project state and suggests prioritized next steps.

## When to Use
- Any time you're unsure what to do next
- Start of a work session
- After completing a task
- When feeling overwhelmed

## Execution Steps

### 1. Load Context

Read these files to understand current state:
- `~/.researchAssistant/researcher_telos.md` (user preferences)
- `.research/project_telos.md` (project state)
- `.research/phase_checklist.md` (phase progress)
- `.research/logs/activity.md` (recent work)
- `tasks.md` (pending tasks)

### 2. First-Time Setup Check

**Check for researcher profile:**
```
IF ~/.researchAssistant/researcher_telos.md does NOT exist:
  - Move ./researcher_telos_template.md to ~/.researchAssistant/researcher_telos.md
  - Ask onboarding questions to populate it
  - Create ~/.researchAssistant/ directory if needed
ELSE:
  - Delete ./researcher_telos_template.md if it still exists
  - Load preferences from existing profile
```

**Check for project setup:**
```
IF .research/project_telos.md is mostly empty (mission not defined):
  - Start project onboarding flow
  - Ask: "What's this project about in 1-2 sentences?"
  - Ask: "Is this part of a larger grant?"
  - Ask: "What's your target output?"
```

### 3. Determine Current Phase

Look at `.research/phase_checklist.md` to identify:
- Which phase is marked as current
- What items are incomplete in current phase
- Whether phase gates are blocking progression

### 4. Run Passive Checks

Silently check for issues (don't show unless found):

| Check | Condition | Message |
|-------|-----------|---------|
| Stale activity | activity.md not updated in >7 days | "It's been a week since your last logged activity." |
| Uncommitted work | `git status` shows changes >3 days old | "You have uncommitted changes. Review and commit?" |
| Undocumented scripts | Scripts in pipeline/scripts/ without docstrings | "Found undocumented scripts." |
| New audio | Files in meetings/ without .md pair | "New meeting recording detected." |
| Orphan figures | Figures not referenced in results.md | "Figure exists but isn't in results." |
| Missing environment | No pyproject.toml/environment.yml | "No environment file detected." |
| Monday check | It's Monday and no weekly review this week | "It's Monday - time for weekly review?" |
| End of day | After 4pm (user's productive time) and no /wrap_up today | "End of day? Run /wrap_up to capture today's progress." |
| Uncommitted notes | /note entries exist without full /wrap_up | "You have notes from today - run /wrap_up to complete the entry?" |

### 5. Generate Prioritized Options

Present 2-4 options in this format:

```
Based on your project state, here are suggested next steps:

A) [Priority indicator] [Action title]
   [Brief explanation of why this matters]
   [Command to run if applicable]

B) [Priority indicator] [Action title]
   [Brief explanation]
   [Command if applicable]

C) [Continue work option if applicable]
   [What they were working on last]

Which would you like to pursue? (Or tell me what you're thinking)
```

**Priority indicators:**
- 🔴 **Critical** - Blocking progress
- 🟡 **High priority** - Should do soon
- 🔵 **Recommended** - Good practice
- ⚪ **Optional** - Nice to have

### 6. Priority Logic

**Order of priority:**
1. First-time setup (profile/project not configured)
2. Phase gate blockers (missing prerequisites)
3. Context gaps (incomplete project_telos sections)
4. Passive check issues (stale work, uncommitted changes)
5. Scheduled reviews (weekly on Monday, monthly on 1st)
6. Continue previous work
7. Next logical step in current phase

### 7. Handle Missing Context

If key context is missing, ask questions instead of assuming:

```
"I'd like to help, but I need a bit more context first:
- What specific aim are you working toward right now?
- What did you accomplish in your last session?"
```

## Example Outputs

### Example 1: New Project
```
Welcome! I see this is a new project. Let's set it up properly.

A) 🔴 Define your project mission
   I need to understand what you're trying to accomplish.
   → I'll ask you a few questions to fill in project_telos.md

B) 🔴 Set up your researcher profile
   No profile found at ~/.researchAssistant/
   → I'll help you create one (takes 2 minutes)

Let's start with (A) - what's this project about?
```

### Example 2: Planning Phase
```
Based on your project state, here are suggested next steps:

A) 🟡 Complete your literature review
   Your background.md is empty but you've defined aims.
   → Run /deep_research on your core concepts

B) 🔵 It's Monday - weekly review?
   No weekly review logged this week.
   → Run /weekly_review

C) ⚪ Continue refining aims
   Your Aim 2 hypothesis is still blank.

Which would you like to pursue?
```

### Example 3: Development Phase with Issues
```
Based on your project state, here are suggested next steps:

A) 🔴 Document your scripts
   I found 3 scripts without docstrings in pipeline/scripts/.
   → Run /review_script to add documentation

B) 🟡 Uncommitted changes detected
   You have changes from 4 days ago. Commit to avoid losing work.
   → Review with `git status` and commit

C) 🔵 Continue pipeline development
   Last session you were working on preprocessing.
   Ready to continue?

Which would you like to pursue?
```

## Related Commands

After /next, users often run:
- `/weekly_review` - If it's start of week
- `/deep_research` - If literature is needed
- `/review_script` - If documentation is flagged
- `/write_methods` - After completing scripts
- `/plan_week` - After weekly review

## Notes

- Always be encouraging, never judgmental
- If user seems stuck, offer to break down the next step
- Remember: user may not know what commands exist - suggest them explicitly
- Update activity.md after significant interactions
