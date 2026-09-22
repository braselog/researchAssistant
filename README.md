# Research Assistant

This repository is a project-aware research workflow for VS Code and GitHub Copilot. It combines project context, reusable Agent Skills, reproducibility conventions, manuscript templates, and lightweight project tracking. It is not a standalone application or VS Code extension.

The assistant uses the files in this repository to help with planning, literature and data work, analysis documentation, manuscript drafting, meetings, and periodic project reviews. Its outputs should remain grounded in the project files and computed results.

## Current State

This checkout is an initial research-project scaffold in the `SETUP` phase:

- Project aims and metadata in `.research/project_telos.md` are still placeholders.
- `scripts/` and `tests/` contain placeholders but no project-specific implementation yet.
- `dvc.yaml` contains commented example stages; there is no active pipeline to reproduce.
- `params.yaml` contains example analysis parameters that should be replaced with project-specific configuration.
- Manuscript files and figure captions are starting templates.

Treat the repository as a foundation for a real project. Do not interpret the example parameters or manuscript text as analysis results.

## Quick Start

### Start from the template

Clone this repository into a new project directory. Replace `[username]` with the GitHub account or organization that owns the template repository.

```bash
git clone https://github.com/[username]/research-assistant-template my-new-project
cd my-new-project
```

If the new project should have its own Git history rather than retaining the template history:

```bash
rm -rf .git
git init
```

### Requirements

- macOS or Linux
- VS Code with GitHub Copilot enabled
- Git
- Conda or another Python environment manager
- Python 3.11 for the supplied environment and CI checks

### Create the environment

```bash
conda env create -f environment.yml
conda activate research-assistant
```

The environment includes Python, DVC, common scientific Python packages, audio tooling, and optional transcription/diarization dependencies. Some features require additional local configuration, such as a Hugging Face token for speaker diarization.

### Configure local settings

```bash
cp .env.example .env
```

Edit `.env` only when using optional integrations such as transcription, speaker diarization, calendar access, local LLM summarization, or GitHub project synchronization. `.env` is ignored by Git and must not contain values that are committed or copied into documentation.

### Open the project

```bash
code .
```

Open GitHub Copilot Chat and start with:

```text
/next
```

`/next` reads the current project state and recommends the highest-value next actions. Before analysis work, update `.research/project_telos.md` and `.research/phase_checklist.md` with the actual research question, aims, and phase.

## How It Works

The assistant has three context layers:

1. **Repository instructions** in `.github/copilot-instructions.md` define the research workflow, reliability expectations, and project-state conventions.
2. **Reusable skills** in `.github/skills/` provide focused workflows for literature, data, statistics, visualization, writing, meetings, planning, reviews, and project coordination.
3. **Project state** in `.research/`, `tasks.md`, `manuscript/`, `data/`, and `results/` supplies the evidence specific to this project.

The researcher profile template in `researcher_telos_template.md` is intended to become the user-level file `~/.researchAssistant/researcher_telos.md`. It stores preferences that can be shared across projects; project aims belong in `.research/project_telos.md`.

## Available Workflows

Use the command name with underscores in Copilot Chat. Each command is implemented by the corresponding skill directory.

### Project state and planning

| Command                 | Purpose                                                        |
| ----------------------- | -------------------------------------------------------------- |
| `/next`                 | Assess project state and recommend next actions.               |
| `/task [description]`   | Add a lightweight task to `tasks.md`.                          |
| `/plan_week`            | Build a focused, calendar-aware weekly plan.                   |
| `/calendar [request]`   | View schedules, find availability, or add approved work blocks |
| `/wrap_up`              | Reconcile the current session with project state.              |
| `/weekly_review`        | Review weekly progress, blockers, and tracking.                |
| `/monthly_review`       | Review progress against aims and deliverables.                 |
| `/quarterly_review`     | Review mission, portfolio, and strategic priorities.           |
| `/sync_project_state`   | Reconcile tasks, decisions, logs, outputs, and GitHub context. |
| `/project_health_check` | Detect stale, inconsistent, or weakly tracked work.            |
| `/record_decision`      | Record a consequential scientific or technical decision.       |
| `/manage_github_work`   | Maintain research-aware GitHub issue and pull-request context. |

### Research and analysis

| Command                                | Purpose                                                       |
| -------------------------------------- | ------------------------------------------------------------- |
| `/deep_research [topic]`               | Search and synthesize literature with verified citations.     |
| `/literature_review [topic]`           | Conduct a documented, multi-source literature review.         |
| `/exploratory_data_analysis [path]`    | Inspect data structure, quality, distributions, and patterns. |
| `/statistical_analysis [question]`     | Plan or perform an appropriate statistical analysis.          |
| `/hypothesis_generation [observation]` | Generate testable hypotheses and predictions.                 |
| `/scientific_visualization [request]`  | Create publication-quality scientific figures.                |
| `/peer_review [document]`              | Evaluate scientific, statistical, and reporting quality.      |

### Manuscript and meeting support

| Command                         | Purpose                                                        |
| ------------------------------- | -------------------------------------------------------------- |
| `/write_background`             | Draft the background from the project's literature files.      |
| `/write_methods`                | Document methods from the implemented pipeline and parameters. |
| `/write_results`                | Draft results from current figures and captions.               |
| `/scientific_writing [request]` | Improve or draft scientific manuscript text.                   |
| `/review_script [path]`         | Review a script for documentation and reproducibility.         |
| `/transcribe [file]`            | Transcribe meeting audio with Whisper.                         |
| `/summarize_meeting [file]`     | Extract meeting decisions, actions, and open questions.        |
| `/note [observation]`           | Record a timestamped observation in the activity log.          |

### Calendar integration

The calendar skill can read calendars visible in macOS Calendar, including iCloud, Exchange/Outlook, and Google calendars. It can show schedules, check availability, and propose research blocks. Adding, moving, or changing an event always requires explicit approval. Calendar configuration and the required wrapper commands are documented in [the calendar skill](.github/skills/calendar/SKILL.md).

## Repository Structure

```text
.
├── .github/
│   ├── copilot-instructions.md       # Research Assistant behaviour and rules
│   ├── hooks/                        # Context-capture hook configuration
│   ├── scripts/                      # Placeholder audits and context capture
│   ├── skills/                       # Reusable research workflows
│   └── workflows/quality.yml         # CI: audit, Ruff, and pytest
├── .research/
│   ├── audits/                       # Audit outputs
│   ├── contracts/                    # Project contracts and expectations
│   ├── inventories/                  # Generated project inventories
│   ├── literature/                   # Literature files and citations
│   ├── logs/                         # Activity, weekly, and monthly logs
│   ├── meetings/                     # Audio and transcript storage
│   ├── notes/                        # Research notes
│   ├── phase_checklist.md            # Phase progress and exit criteria
│   └── project_telos.md              # Aims, scope, risks, and current state
├── data/
│   ├── raw/                          # Immutable source data
│   ├── processed/                    # Derived data
│   └── README.md                     # Data governance and provenance rules
├── manuscript/                       # Background, methods, results, discussion
│   └── figures/                      # Publication figures and captions
├── results/                          # Generated outputs and metrics
├── scripts/                          # Project-specific analysis code
├── tests/                            # Automated validation and fixtures
├── dvc.yaml                          # Reproducible pipeline stages
├── environment.yml                   # Conda environment definition
├── params.yaml                       # Centralized pipeline parameters
├── PROJECT_README.md                 # Project-specific README template
├── researcher_telos_template.md      # User profile template
└── tasks.md                          # Lightweight project task queue
```

The `data/raw/`, `data/processed/`, and sensitive-data locations are ignored by default. Keep raw data immutable, document provenance, and use DVC or an approved storage system for large or restricted data. Never commit credentials or sensitive research data.

## Reproducibility

The intended analysis workflow is:

```text
data/raw/ -> scripts/ -> data/processed/ -> results/ -> manuscript/figures/
```

When project-specific scripts exist, define their dependencies, parameters, and outputs in `dvc.yaml`. Keep tunable values in `params.yaml`, document the implementation in `manuscript/methods.md`, and generate results rather than editing them manually.

The current repository has no active DVC stages. After adding stages and configuring a DVC remote where needed, the normal commands are:

```bash
dvc status
dvc repro
dvc metrics show
```

Use `dvc pull` only after a project DVC remote has been configured and data or outputs have been published there.

## Quality Checks

The GitHub Actions workflow in `.github/workflows/quality.yml` runs on pushes and pull requests:

```bash
python .github/scripts/audit_placeholders.py
ruff check .
pytest
```

The placeholder audit is useful during setup because it identifies template content that still needs project-specific values. Install `ruff` and `pytest` in the active environment if they are not already available. Before committing, the configured pre-commit hooks can be run with:

```bash
pre-commit run --all-files
```

## Where to Add Project Content

1. Define the mission, aims, risks, and current phase in `.research/project_telos.md`.
2. Mark completed setup work in `.research/phase_checklist.md` and keep `tasks.md` focused on short actions.
3. Replace the placeholders in `PROJECT_README.md` with the project question, data sources, pipeline stages, outputs, and limitations.
4. Add provenance for every source dataset under `data/raw/`; place derived data under `data/processed/`.
5. Add documented scripts under `scripts/`, tests under `tests/`, and active stages to `dvc.yaml`.
6. Keep `manuscript/methods.md`, figures, captions, results, and discussion synchronized with the actual analysis.

## Related Documentation

- [Project README template](PROJECT_README.md)
- [Research Assistant instructions](.github/copilot-instructions.md)
- [Phase checklist](.research/phase_checklist.md)
- [Project aims and state](.research/project_telos.md)
- [Data management rules](data/README.md)
- [Results organization](results/README.md)
- [Script conventions](scripts/README.md)
- [Calendar integration](.github/skills/calendar/SKILL.md)
- [Environment definition](environment.yml)
- [Pipeline configuration](dvc.yaml)
- [Quality workflow](.github/workflows/quality.yml)
