---
name: _commit-context
description: Internal verification step executed before every agent response to determine what information should be logged to project files for context preservation.
---

# Commit Context to Memory

## Purpose

This is an **automatic internal skill** that runs before every agent response (except during active skill execution). It ensures critical information from the conversation is captured in the appropriate project files for future context.

## When to Execute

**Automatically run this check:**
- Before sending ANY response to the user (except when already executing a skill)
- After completing a skill that generated decisions or information
- After user shares important context about their work

**Do NOT run:**
- During initial setup (_setup-guard)
- While actively executing another skill (avoid recursion)
- When the user's message is purely conversational with no actionable content

## Information Routing Logic

Use this decision tree to determine what goes where:

### 1. Tasks (tasks.md)

**When to add:**
- User mentions something they need to do
- Agent suggests an action that requires user implementation
- Meeting summary extracts action items
- Script review identifies needed changes
- Analysis reveals next analysis steps

**Criteria:**
- < 2 hours of work
- Single, specific action
- Doesn't require branching/comparison
- Has a clear done state

**Format:**
```markdown
- [ ] [Action verb] [specific thing] [optional: in/for X]
```

**Examples that should be tasks:**
- "Fix the docstring in preprocess.py"
- "Add error handling to data loader"
- "Update methods.md with new preprocessing step"
- "Run exploratory analysis on new dataset"

### 2. Activity Log (.research/logs/activity.md)

**When to add:**
- Significant work was completed (file created, analysis run, section written)
- Important decision was made about project direction
- User shares what they accomplished in a session
- A phase gate was passed
- Pipeline was modified

**Criteria:**
- Represents completed work (not future intentions)
- Provides context for "what happened when"
- Would help the RA understand project state later
- Documents why a choice was made

**Format:**
```markdown
## [YYYY-MM-DD HH:MM]

**Context**: [1-line summary]

**What changed**:
- [Specific outcomes]

**Decisions made**:
- [If applicable]
```

**Examples that should be logged:**
- "Completed literature review on [topic], identified 15 relevant papers"
- "Decided to use regression instead of classification based on data distribution"
- "Wrote first draft of background section covering [topics]"
- "Refactored preprocessing pipeline to handle missing data"

### 3. Quick Notes (.research/notes/[topic].md)

**When to create/append:**
- User shares an idea or hypothesis to explore later
- Interesting finding that isn't a task or completed work
- Reference information to remember (URLs, citations, concepts)
- Context about why something matters
- Questions to investigate

**Criteria:**
- Doesn't have a clear "done" state (not a task)
- Not yet actionable or implemented (not activity)
- Worth remembering for later
- Provides reasoning or background

**Format:**
```markdown
## [YYYY-MM-DD] [Title]

[Content]

[Optional: Related to: [task/file/section]]
```

**Examples that should be notes:**
- "Consider using Bayesian approach if frequentist assumptions don't hold"
- "Paper by Smith et al. suggests alternative interpretation of our results"
- "Hypothesis: preprocessing method may introduce bias for small samples"
- "Reminder: grant requires specific figure format for submission"

### 4. README.md / PROJECT_README.md

**When to update:**
- Project structure changes significantly
- New major component added (pipeline stage, analysis module)
- Dependency requirements change
- Installation/setup process changes
- Project scope or aims evolve

**Criteria:**
- Affects onboarding (someone cloning the repo needs to know)
- Changes how to run the project
- Structural/architectural decisions

**Examples:**
- Added new data source requiring authentication
- Split analysis into separate modules
- Added new dependency requiring conda environment update
- Changed from single script to DVC pipeline

## Execution Steps

### Step 1: Analyze the Conversation

Review the current exchange and identify:
1. What actionable items emerged?
2. What decisions were made?
3. What context was shared about work done?
4. What ideas or hypotheses were discussed?
5. Did any project structure change?

### Step 2: Route Information

For each piece of information identified, determine the target file(s):

**Tasks:**
- Check if item is < 2 hours, specific, actionable
- Add to appropriate priority section in tasks.md

**Activity:**
- Check if this represents completed work or a decision
- Append entry to .research/logs/activity.md

**Notes:**
- Check if this is reference info, ideas, or future considerations
- Create/append to .research/notes/[relevant-topic].md

**README:**
- Check if this changes project structure or setup
- Update README.md or PROJECT_README.md

### Step 3: Execute Updates

If any updates are needed:
1. Read the current file
2. Add new content in appropriate location
3. Maintain existing format
4. Be concise but specific

### Step 4: Notify User (Subtly)

**If updates were made:**
Add a brief, subtle footer to your response:
```
📝 *[Logged to activity] / [Added task] / [Noted in .research/notes/[topic].md]*
```

**If no updates needed:**
No notification - just respond normally.

## Special Cases

### Case: User Rejects or Modifies

If the user says "no, that's not what I meant" or provides correction:
- Do NOT log the incorrect interpretation
- Wait for clarification before routing

### Case: Information Already Captured

If the item is already in tasks.md or was recently logged:
- Do NOT duplicate
- Optionally update if new details emerged

### Case: Sensitive Information

If the user shares personal/sensitive context:
- Log to activity.md or notes ONLY if relevant to research decisions
- Keep it professional and research-focused

### Case: Large Multi-Step Work

If the conversation covered completing multiple phases:
- Break into separate activity log entries by date/session
- Add individual tasks that remain
- Create notes for open questions

## Examples

### Example 1: User Reports Completing Work

**User**: "I finished running the preprocessing pipeline and it generated the cleaned dataset in data/processed/. Took about 3 hours but found some outliers I wasn't expecting."

**Route**:
- **Activity log**: "Completed preprocessing pipeline run, generated cleaned dataset in data/processed/. Identified unexpected outliers requiring investigation."
- **Tasks**: "- [ ] Investigate outliers identified in preprocessing"
- **Notes**: (.research/notes/data-quality.md) "## [Date] Outliers Found\nPreprocessing revealed unexpected outliers - check if data entry errors or real signal. Located in [specific columns/rows if mentioned]."

### Example 2: User Asks for Analysis Help

**User**: "Can you help me choose between t-test and Mann-Whitney U test for comparing these two groups?"

**Route**:
- **None** - This is a consultation, not work done yet
- Provide answer, then IF you run the analysis together, log the decision to activity.md

### Example 3: User Shares Hypothesis

**User**: "I'm wondering if the low correlation might be because we're not accounting for the time lag effect."

**Route**:
- **Notes**: (.research/notes/hypotheses.md) "## [Date] Time Lag Hypothesis\nLow correlation may be due to unaccounted time lag effect. Consider lagged correlation analysis."
- **Tasks**: "- [ ] Test correlation with lagged variables"

### Example 4: You Suggest Script Changes

**Agent**: "I see the issue - the data loader doesn't handle missing values. You could add a .dropna() call or use .fillna(). Which would fit your analysis better?"

**Route**:
- **Tasks** (after user decides): "- [ ] Add missing value handling to data loader (using [chosen method])"

## Critical Don'ts

1. **DON'T log every conversational exchange** - Only capture actionable/significant items
2. **DON'T duplicate** - Check if it's already captured
3. **DON'T log during skill execution** - Let the skill handle its own logging
4. **DON'T break flow** - This should be invisible/quick
5. **DON'T make assumptions** - If unclear what the user meant, ask before logging

## Integration with Existing Skills

Some skills already handle their own logging:
- `/wrap-up` → Explicitly logs to activity.md
- `/weekly-review` → Creates review log
- `/note [text]` → Creates note directly
- `/task [text]` → Adds to tasks.md directly

When these skills run, _commit-context should NOT duplicate their work.

## Verification Checklist

Before responding to user, quickly verify:
- [ ] Did actionable tasks emerge? → tasks.md
- [ ] Was work completed? → activity.md  
- [ ] Were decisions made? → activity.md
- [ ] Were ideas/hypotheses shared? → notes/
- [ ] Did structure change? → README

Then respond.

---

**Remember**: This skill should feel invisible. The goal is keeping the project organized without interrupting the conversation flow.
