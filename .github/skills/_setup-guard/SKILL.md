---
name: _setup-guard
description: INTERNAL. Mandatory pre-flight check that runs before any other skill to ensure user profile and project are configured. Auto-invokes on first interaction.
---

# Setup Guard

**Purpose**: Ensure user and project are configured before allowing any other operations. This skill is automatically invoked before processing any user request.

**Returns**: 
- PROCEED (setup complete)
- SETUP_COMPLETE (just finished setup, ready to proceed)

## Execution Steps

### Step 1: Check User Profile

Check if `~/.researchAssistant/researcher_telos.md` exists.
(Use `cat ~/.researchAssistant/researcher_telos.md` in terminal - file is outside workspace)

**IF it does NOT exist:**

1. **Copy template to user directory:**
   - Create directory: `~/.researchAssistant/`
   - Copy `./researcher_telos_template.md` to `~/.researchAssistant/researcher_telos.md`
   - Delete `./researcher_telos_template.md` from project root (cleanup)

2. **Show welcome message:**
   ```
   🚀 Welcome to Research Assistant!
   
   I notice this is your first time using RA. Let's take 2-3 minutes to set up your profile.
   This will help me give you personalized guidance across all your research projects.
   
   I'll ask you 4 quick questions:
   ```

3. **Run user onboarding questions:**
   
   Ask these one at a time, wait for response, then update `~/.researchAssistant/researcher_telos.md`:
   
   - "**When are you most productive?** (morning / afternoon / evening / flexible)"
   - "**What's your preferred environment manager?** (uv / conda / venv / not sure)"
   - "**What's your primary programming language?** (Python / R / both / other)"
   - "**Any particular weaknesses you want me to help with?**
     Examples: documentation, committing often, scope creep, writing, organization, planning"

4. **Update the file** with their responses (replace template placeholders)

5. **Confirm completion:**
   ```
   ✓ Profile saved to ~/.researchAssistant/researcher_telos.md
   
   You can update this anytime by editing that file directly.
   Now let's set up your project...
   ```

6. **Proceed to Step 2**

**IF it DOES exist:**

1. **Load the profile** for context

2. **Check for incomplete sections** (containing "TODO:"):
   - Read the entire file content
   - Search for any lines containing "[TODO:"

3. **If TODOs are found:**
   - Show message: "I see your profile needs some updates. Let's complete the missing sections."
   - For each TODO found, ask an appropriate question to fill it in.
   - Update the file by replacing each "[TODO: ...] with the user's response
   - Update the "Last updated" date to today
   - Show completion message: "✓ Profile updated and complete!"

4. **If no TODOs found:**
   - Profile is complete, proceed to Step 2

---

### Step 2: Check Project Setup

Check if `.research/project_telos.md` exists AND is filled out (mission is NOT "[TODO:" or empty).

**IF it does NOT exist OR is a template:**

1. **Show project setup message:**
   ```
   📋 New Project Setup
   
   Let's define this project's goals and scope.
   I'll ask you 4 quick questions:
   ```

2. **Ensure `.research/` directory exists:**
   - If not, create it along with subdirectories:
     - `.research/literature/`
     - `.research/meetings/audio/`
     - `.research/meetings/transcripts/`
     - `.research/logs/weekly/`
     - `.research/logs/monthly/`

3. **Run project onboarding questions:**
   
   Ask these one at a time, wait for response:
   
   - "**What's this project about in 1-2 sentences?**"
   - "**Is this part of a larger grant?** If so, which specific aim does it address? (or 'no' / 'independent')"
   - "**What's your target output?** (journal paper / thesis chapter / tool / conference paper / other)"
   - "**Do you have any collaborators or a PI to report to?** (names or 'just me')"

4. **Create or update `.research/project_telos.md`:**
   ```markdown
   # Project Telos
   
   > This file defines the aims, scope, and current state of this research project.
   
   ## Mission
   
   [Their 1-2 sentence description]
   
   ## Grant Context
   
   [Their grant/aim info or "Independent research project"]
   
   ## Target Output
   
   [journal paper / thesis chapter / etc.]
   
   ## Collaborators
   
   [Names or "Solo project"]
   
   ## Current Phase
   
   **Phase**: SETUP
   **Started**: [today's date]
   **Last Updated**: [today's date]
   
   ## Aims
   
   [To be filled in during PLANNING phase]
   
   ## Background Context
   
   [To be filled in during PLANNING phase]
   
   ## Methods Overview
   
   [To be filled in during DEVELOPMENT phase]
   
   ## Progress Notes
   
   - [today's date]: Project initialized
   ```

5. **Create `.research/phase_checklist.md`:**
   ```markdown
   # Phase Checklist
   
   > Tracks completion of phase-specific requirements
   
   ## SETUP Phase
   
   - [x] Project initialized
   - [x] .research/ structure created
   - [x] project_telos.md defined
   - [ ] Git repository initialized
   - [ ] Environment configured
   - [ ] DVC initialized (if using)
   
   ## PLANNING Phase
   
   - [ ] Research aims defined
   - [ ] Hypothesis articulated
   - [ ] Literature review begun
   - [ ] background.md drafted
   
   ## DEVELOPMENT Phase
   
   - [ ] Pipeline structure defined
   - [ ] Key scripts created
   - [ ] Data acquisition documented
   - [ ] Scripts have docstrings
   
   ## ANALYSIS Phase
   
   - [ ] Pipeline running successfully
   - [ ] Results generated
   - [ ] Figures created with captions
   
   ## WRITING Phase
   
   - [ ] All manuscript sections drafted
   - [ ] Methods reflect current scripts
   - [ ] Figures integrated into results
   
   ## REVIEW Phase
   
   - [ ] Self-review completed
   - [ ] Reproducibility verified
   - [ ] Ready for submission
   ```

6. **Create `.research/logs/activity.md`:**
   ```markdown
   # Activity Log
   
   > Running log of research activities, decisions, and progress
   
   ## [today's date]
   
   **Phase**: SETUP
   
   - Project initialized: [project mission from above]
   - Target output: [target output from above]
   ```

7. **Confirm completion:**
   ```
   ✓ Project set up in .research/
   
   You're now in the SETUP phase. Next steps:
   - Initialize git repository (if not done)
   - Set up your environment
   - Run /next to see recommended actions
   ```

**IF it DOES exist and is filled out:**
- Load the project context (for reference)
- Proceed to Step 3

---

### Step 3: Return Status

Return `SETUP_COMPLETE` if any setup was performed, or `PROCEED` if setup was already complete.

---

## Notes

- This skill runs automatically before ANY user interaction
- Cannot be skipped or bypassed
- Template cleanup happens automatically (researcher_telos_template.md deleted after copy)
- All other skills should assume this has already run
- User profile persists across all projects (~/.researchAssistant/)
- Project setup is per-project (.research/ in project root)
