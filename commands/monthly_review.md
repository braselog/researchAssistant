# /monthly_review Command

> Conduct a monthly review of project alignment and progress toward aims.

## When to Use
- First week of each month (RA will prompt)
- After completing a major milestone
- When feeling uncertain about direction
- Before reporting to PI/collaborators

## Execution Steps

### 1. Gather Context

Read these files:
- `.research/project_telos.md` - Aims and goals
- `.research/phase_checklist.md` - Phase progress
- `.research/logs/weekly/*.md` - All weekly reviews this month
- `.research/logs/monthly/` - Previous monthly reviews
- `manuscript/` - Manuscript progress
- Git log for the month

### 2. Generate Monthly Review

```markdown
# Monthly Review: [MONTH YEAR]

## Executive Summary

**Project**: [Project name from project_telos.md]
**Current Phase**: [PHASE]
**Overall Health**: 🟢 On Track / 🟡 Needs Attention / 🔴 At Risk

## Progress Against Aims

### Aim 1: [Title]
- **Status**: [Not started / In progress / Complete]
- **Progress this month**: 
  - [Specific accomplishment]
  - [Specific accomplishment]
- **Blockers**: [None / List]
- **On track for completion?**: [Yes/No - by when]

### Aim 2: [Title]
- **Status**: 
- **Progress this month**: 
- **Blockers**: 
- **On track?**: 

### Aim 3: [Title]
[Continue pattern]

## Phase Progress

| Phase | Last Month | This Month | Change |
|-------|------------|------------|--------|
| SETUP | ✅ | ✅ | - |
| PLANNING | 80% | ✅ | Completed |
| DEVELOPMENT | 20% | 60% | +40% |
| ANALYSIS | 0% | 10% | Started |
| WRITING | 0% | 0% | - |
| REVIEW | 0% | 0% | - |

## Manuscript Status

| Section | Status | Last Updated |
|---------|--------|--------------|
| Background | [Draft/Revision/Complete] | [Date] |
| Methods | [Draft/Revision/Complete] | [Date] |
| Results | [Draft/Revision/Complete] | [Date] |
| Discussion | [Not started/Draft/Complete] | [Date] |

## Key Metrics

### Productivity Dashboard
| Metric | Target | Achieved | YTD Total |
|--------|--------|----------|----------|
| Weekly reviews completed | 4 | | |
| Active coding days | 15 | | |
| Commits | 20 | | |
| Scripts documented | | | |
| Figures generated | | | |
| Manuscript sections drafted | | | |

### Pipeline
- Weekly reviews completed: [X/4 or 5]
- Active coding days: [N] days
- Commits: [N]
- Scripts documented: [N/Total]

### Pipeline
- DVC stages defined: [N]
- Pipeline runs successfully: [Yes/No]
- Figures generated: [N]

### Off-Track Indicators

Check for these warning signs:

- [ ] Behind schedule by >2 weeks on milestones
- [ ] Budget/resource concerns emerging
- [ ] Equipment or infrastructure issues
- [ ] Collaboration or communication problems
- [ ] Unexpected results requiring a pivot
- [ ] Scope creeping beyond original aims
- [ ] External deadlines at risk (conferences, grants)
- [ ] Key decisions being postponed repeatedly

**If 2+ boxes checked**: Consider pause and reassessment. See "When Off-Track" section below.

## Wins This Month 🎉
1. [Major accomplishment]
2. [Progress to celebrate]
3. [Something that went well]

## Challenges & Lessons

### What Didn't Go as Planned
- [Challenge or setback]
- [What was learned]

### Adjustments Made
- [Any pivots or changes to approach]

### Root Cause Analysis (When Off-Track)

If significant issues identified, complete this table:

| Issue | Root Cause | Corrective Action | Owner | Check-In Date |
|-------|------------|-------------------|-------|---------------|
| [Problem] | [Why it happened] | [What will change] | [Who's responsible] | [When to reassess] |
| | | | | |
| | | | | |

**Common Root Causes:**
- Unclear requirements or scope
- Technical complexity underestimated
- External dependencies not accounted for
- Skill gap requiring learning time
- Competing priorities or distractions
- Insufficient planning or buffers

## Alignment Check

### Original Goals vs Current Direction
Are we still aligned with the project mission?

**Mission**: [From project_telos.md]
**Current work**: [What we're actually doing]
**Alignment**: 🟢 Strong / 🟡 Drifting / 🔴 Misaligned

### If Misaligned
- **Cause**: [Why the drift?]
- **Options**:
  A) Realign work to original aims
  B) Update aims to reflect new direction
  C) Split into separate project

## Next Month's Focus

### Top 3 Priorities
1. [Priority 1] - [Why important]
2. [Priority 2] - [Why important]
3. [Priority 3] - [Why important]

### Goals for Next Month
- [ ] [Specific, measurable goal]
- [ ] [Specific, measurable goal]
- [ ] [Specific, measurable goal]

### Anticipated Challenges
- [What might get in the way]
- [How to mitigate]

## Resource Needs

### Help Needed
- [Collaboration, feedback, resources needed]

### Decisions Pending
- [Decisions that need to be made]

---

*Review completed: [TIMESTAMP]*
*Next monthly review due: [DATE]*
*Related: See weekly reviews in .research/logs/weekly/*
```

### 3. Interactive Components

Ask the user:
```
Time for your monthly review. Let's reflect on [MONTH]:

1. What was your biggest accomplishment this month?
2. What's your current confidence level (1-5) that you'll meet your project goals?
3. Has your understanding of the problem changed? If so, how?
4. Is there anything you've been avoiding or procrastinating on?
5. What do you need to make next month successful?
```

### 4. Trend Analysis

Compare to previous months:

```markdown
## Trend Analysis

### Phase Velocity
- Month 1: SETUP → PLANNING
- Month 2: PLANNING → DEVELOPMENT (started)
- Month 3: DEVELOPMENT (60%) ← Current

**Trajectory**: [On pace / Ahead / Behind]

### Recurring Blockers
[Blockers that appear across weeks/months]

### Improvement Areas
[Consistent challenges across reviews]
```

### 5. Save and Update

- Save to `.research/logs/monthly/YYYY-MM.md`
- Update project_telos.md with any aim status changes
- Flag for quarterly review if pattern issues detected

### 6. Next Steps

```
Monthly review saved to .research/logs/monthly/[MONTH].md

Based on your review:

A) 🎯 Update project aims
   [If alignment issues detected]

B) 📋 Plan next month's sprints
   Break priorities into weekly goals

C) 📧 Draft progress report
   For PI/collaborators if applicable

D) 🔄 Continue with current work
   You're on track - keep going!

What would you like to do?
```

## Related Commands

- `/weekly_review` - More granular progress tracking
- `/quarterly_review` - Bigger picture assessment
- `/next` - Get next suggestion

## Notes

- Monthly reviews are about direction, not just progress
- It's okay to change direction if justified
- Honest assessment > optimistic reporting
- Compare trends, not just current state
