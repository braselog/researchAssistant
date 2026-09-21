# [Project title]

[One-sentence description of the research question, system, dataset, and intended contribution.]

## Project Status

- **Research aim:** [AIM-1 or concise aim]
- **Current stage:** [Setup / Planning / Development / Analysis / Writing / Review]
- **Target output:** [Journal article / Thesis chapter / Software / Dataset / Report]
- **Primary contact:** [Name and contact]
- **Last major update:** [YYYY-MM-DD]

For detailed aims, scope, decisions, and current state, see `.research/project_telos.md`.

## Overview

### Research question

[State the primary question or hypothesis in language understandable to someone in the field who is new to the project.]

### Rationale

[Explain why the question matters, what gap it addresses, and what is distinctive about this project.]

### Approach

[Summarize the data, experimental or computational design, and major analysis stages.]

### Expected outputs

- [Primary scientific output]
- [Pipeline, model, dataset, or resource]
- [Manuscript, figures, or report]

## Reproducing the Project

### 1. Clone the repository

```bash
git clone [repository-url]
cd [project-name]
```

### 2. Create the environment

Use the environment definition included in this repository. Replace the example below if this project uses `uv`, `venv`, `renv`, containers, or another system.

```bash
conda env create -f environment.yml
conda activate research-assistant

# Optional transcription environment
# conda env create -f environment-transcription.yml
```

### 3. Configure local settings

```bash
cp .env.example .env
```

Add only required local paths, tokens, or service settings. Never commit `.env`.

### 4. Obtain the data

If data are managed through a DVC remote:

```bash
dvc pull
```

Otherwise, follow the access instructions in [Data](#data). Restricted data are not included in the repository.

### 5. Reproduce the pipeline

```bash
dvc status
dvc repro
```

Inspect tracked metrics where applicable:

```bash
dvc metrics show
```

### 6. Run validation

```bash
[project test command]
[project lint or validation command]
```

A clean pipeline execution should produce the outputs described under [Outputs](#outputs). Any external services, hardware requirements, or non-deterministic stages should be documented below.

## Pipeline

The implemented workflow is defined in `dvc.yaml`, with parameters in `params.yaml` and reproduced state in `dvc.lock`.

| Stage | Purpose | Main inputs | Main outputs |
|---|---|---|---|
| `[stage-name]` | [What the stage does] | `[input paths]` | `[output paths]` |
| `[stage-name]` | [What the stage does] | `[input paths]` | `[output paths]` |

Update this table when the high-level workflow changes. Detailed implementation belongs in code, configuration, and `manuscript/methods.md`.

## Data

### Sources

| Dataset | Source | Access | Version or date |
|---|---|---|---|
| [Dataset] | [Repository, consortium, or experiment] | [Public / controlled / local] | [Version/date] |

### Data organization

```text
data/
├── raw/          # Original, immutable inputs
├── processed/    # Derived or cleaned data
└── .sensitive/   # Restricted local data, excluded from Git and Copilot
```

### Governance and restrictions

[Describe consent, licenses, data-use agreements, access controls, de-identification, or restrictions relevant to reuse. Do not place sensitive details or credentials in this file.]

## Repository Structure

```text
.
├── .github/
│   ├── copilot-instructions.md       # Research Assistant behaviour
│   ├── hooks/                        # Agent lifecycle hooks
│   ├── scripts/                      # Hook and validation scripts
│   └── skills/                       # Research workflows
├── .research/
│   ├── project_telos.md              # Aims, scope, and current state
│   ├── phase_checklist.md            # Phase-oriented progress guide
│   ├── decisions/                    # Scientific and technical decisions
│   ├── literature/                   # Literature outputs and citations
│   ├── meetings/                     # Meeting audio, transcripts, summaries
│   ├── traceability/                 # Evidence underlying manuscript claims
│   └── logs/                         # Activity and periodic reviews
├── data/                              # Raw and derived data
├── scripts/                           # Analysis and pipeline code
├── tests/                             # Automated validation
├── results/
│   ├── intermediate/
│   ├── final/
│   ├── metrics/
│   └── logs/
├── manuscript/
│   ├── background.md
│   ├── methods.md
│   ├── results.md
│   ├── discussion.md
│   └── figures/
├── dvc.yaml
├── dvc.lock
├── params.yaml
└── tasks.md
```

Adjust this section to reflect the actual repository rather than preserving unused template directories.

## Outputs

| Output | Location | Description |
|---|---|---|
| [Primary result] | `results/final/[file]` | [Description] |
| [Figure set] | `manuscript/figures/` | [Description] |
| [Model or resource] | `[path]` | [Description] |

For manuscript traceability, `.research/traceability/manuscript-evidence.md` links important methods and claims to source code, parameters, DVC stages, outputs, and figures.

## Key Decisions and Limitations

Consequential decisions are recorded under `.research/decisions/`. Summarize only the decisions readers need to understand the project:

- [Decision and concise rationale]
- [Known limitation or trade-off]
- [Condition that would require reassessment]

## Using the Research Assistant

This repository includes VS Code GitHub Copilot instructions, Agent Skills, and optional hooks that provide project-aware research support.

Useful entry points:

```text
/next                         Assess project state and recommend next actions
/plan_week                    Build a calendar-aware weekly plan
/wrap_up                      Reconcile daily context and project state
/summarize_meeting [file]     Extract meeting decisions and actions
/review_script [path]         Review code and analytical reliability
/write_methods                Draft methods from implementation and DVC state
/write_results                Draft results from current outputs and figures
/weekly_review                Review weekly progress and blockers
```

The assistant treats:

- `tasks.md` as the lightweight personal action queue;
- GitHub issues as substantial repository work;
- `.research/decisions/` as durable rationale;
- meeting and activity logs as historical evidence;
- DVC and computed outputs as the source of truth for reproducibility;
- `.research/traceability/manuscript-evidence.md` as the internal evidence map for manuscript claims.

Temporary context captured during Copilot sessions is reconciled by `/wrap_up` and should not be committed as authoritative project documentation.

## Development and Contribution

### Branching and review

[Describe the branch naming, pull-request, review, and merge conventions used by the project.]

### Quality checks

Before submitting changes:

```bash
[project formatting command]
[project lint command]
[project test command]
dvc status
```

Substantial changes should link to the relevant GitHub issue and, where appropriate, a decision record.

### Reporting problems

Use GitHub issues for reproducible bugs, substantial analysis changes, or work requiring discussion and review. Use `tasks.md` for lightweight personal actions.

## Results and Manuscript

- **Methods:** `manuscript/methods.md`
- **Results:** `manuscript/results.md`
- **Figures:** `manuscript/figures/`
- **Evidence map:** `.research/traceability/manuscript-evidence.md`
- **Current manuscript status:** [Drafting / Internal review / Submitted / Published]

Do not report results in this README unless they are stable, current, and supported by reproduced outputs.

## Citation

If this repository or its outputs are used, cite:

```bibtex
@article{[citation-key],
  author  = {[Authors]},
  title   = {[Title]},
  journal = {[Journal]},
  year    = {[Year]},
  doi     = {[DOI]}
}
```

For software or datasets, add the appropriate DOI, release, archived repository, or citation file.

## License

[Specify the software, data, and documentation licenses. Note any components governed by separate terms.]

## Contact

[Name]  
[Institution or group]  
[Email or project contact]

---

This project was initialized from the Research Assistant Template. Remove this note if it is not useful to project readers.
