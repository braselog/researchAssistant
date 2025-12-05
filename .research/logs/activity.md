# Activity Log

> Running log of project activity. Updated after significant work sessions.
> The Research Assistant uses this to understand recent context.

---

## Quick Session Entry Template

```markdown
## [YYYY-MM-DD]

**Session focus**: [What you worked on]

**Accomplished**:
- [What was completed]

**Decisions made**:
- [Any choices or directions taken]

**Next steps**:
- [What to do next]

**Notes**:
- [Any other context]
```

---

## Lab Notebook Entry Template (For Experimental Work)

Use this format when documenting experiments, analyses, or pipeline runs:

```markdown
## [YYYY-MM-DD] - [Experiment/Analysis Name]

### Objective
[What you're trying to accomplish in 1-2 sentences]

### Protocol/Method
[Key steps or deviations from standard protocol]
- Used parameters: [list key settings from params.yaml]
- Modified from standard: [any changes]

### Observations
[What happened, including unexpected events]
- Runtime: [how long it took]
- Warnings/errors: [any issues encountered]

### Data/Outputs
[Where outputs are stored]
- Output files: `results/[filename]`
- Figures generated: `manuscript/figures/[figN]/`

### Preliminary Conclusions
[Initial interpretation - can be updated later]

### Next Steps
[What to do based on these results]

### Cross-References
- Related scripts: `pipeline/scripts/[name].py`
- Related params: `params.yaml` section `[section]`
- Related issue: #[issue number]
```

---

## File Naming Convention

Use consistent naming for all project files:

```
YYYYMMDD_experiment_condition_version.ext

Examples:
20241202_qpcr_treatment_v01.csv
20241202_preprocessing_output_v02.csv
20241202_figure1_draft.png
```

**Rules:**
- Use ISO date format (YYYYMMDD) for sortability
- Use underscores, never spaces
- Include version numbers for iterations
- Keep names descriptive but concise

---

## Digital Documentation Standards

### Core Principles
1. **Date everything** - ISO format (YYYY-MM-DD) for sorting
2. **Never overwrite** - Create new versions instead of modifying
3. **Cross-reference** - Link notebook entries to scripts and data files
4. **Back up regularly** - Follow 3-2-1 rule: 3 copies, 2 media types, 1 offsite

### Version Control Integration
- Commit at least daily when actively working
- Reference notebook entries in commit messages
- Tag versions before major analyses: `git tag -a v1.0 -m "Pre-analysis checkpoint"`

---

<!-- 
Add new entries at the top.
Keep entries brief but informative.
The RA will prompt you to update this after significant sessions.
-->
