# Project Title

> A reproducible research project powered by the Research Assistant (RA)

[![DVC](https://img.shields.io/badge/DVC-tracked-blue)](https://dvc.org)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Quick Start

1. **Clone this repository**
   ```bash
   git clone [repository-url]
   cd [project-name]
   ```

2. **Set up environment**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using conda
   conda env create -f environment.yml
   conda activate [project-name]
   ```

3. **Run the pipeline**
   ```bash
   dvc repro
   ```

4. **Get started with the Research Assistant**
   Open in VS Code with GitHub Copilot enabled, then type:
   ```
   /next
   ```

## Project Overview

**Mission**: [Describe your research question/goal]

**Status**: [Current phase: SETUP / PLANNING / DEVELOPMENT / ANALYSIS / WRITING / REVIEW]

**Target Output**: [Journal paper / Thesis chapter / Tool]

## Repository Structure

```
.
├── .github/
│   └── copilot-instructions.md   # Research Assistant configuration
├── .research/
│   ├── project_telos.md          # Project aims and state
│   ├── phase_checklist.md        # Progress tracking
│   ├── literature/               # Literature reviews and citations
│   └── logs/                     # Activity and review logs
├── commands/                     # Slash command definitions
├── data/
│   ├── raw/                      # Original, immutable data
│   ├── processed/                # Cleaned/transformed data
│   └── .sensitive/               # Private data (not tracked)
├── scripts/                      # Analysis and utility scripts
├── results/                      # Pipeline outputs and metrics
│   ├── intermediate/             # Intermediate stage outputs
│   ├── final/                    # Final analysis results
│   ├── metrics/                  # DVC-tracked metrics
│   └── logs/                     # Execution logs
├── manuscript/
│   ├── background.md
│   ├── methods.md
│   ├── results.md
│   ├── discussion.md
│   └── figures/                  # Figures with captions
├── meetings/                     # Meeting transcripts and notes
├── dvc.yaml                      # Pipeline definition
├── params.yaml                   # Pipeline parameters
├── tasks.md                      # Current tasks
└── README.md                     # This file
```

## Using the Research Assistant

This project template includes context files that guide VS Code's GitHub Copilot to act as a Research Assistant (RA). The RA helps you:

- **Stay on track**: Guides you through research phases
- **Write better**: Drafts manuscript sections from your work
- **Stay organized**: Tracks tasks and action items
- **Stay reproducible**: Ensures proper documentation

### Key Commands

| Command | Purpose |
|---------|---------|
| `/next` | Get suggested next steps (catch-all for beginners) |
| `/deep_research [topic]` | Literature search with citations |
| `/write_background` | Draft background from literature |
| `/write_methods` | Document scripts as methods |
| `/write_results` | Draft results from figures |
| `/review_script [path]` | Check code documentation |
| `/weekly_review` | Weekly progress review |
| `/plan_week` | Create weekly plan |
| `/transcribe [file]` | Transcribe meeting audio |
| `/summarize_meeting [file]` | Extract action items |

### Getting Started

1. Open VS Code with GitHub Copilot enabled
2. Type `/next` in the chat
3. Follow the RA's guidance to set up your project

## Reproducing This Work

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) or conda
- [DVC](https://dvc.org/) 3.0+
- Git

### Full Reproduction

```bash
# Clone and enter repository
git clone [repository-url]
cd [project-name]

# Set up environment
uv sync

# Pull data (if using DVC remote)
dvc pull

# Run complete pipeline
dvc repro

# Figures will be generated in manuscript/figures/
```

### Verify Outputs

```bash
# Check pipeline status
dvc status

# Compare metrics
dvc metrics show
```

## Data

**Source**: [Describe where data comes from]

**Access**: [How to obtain the data]

**Sensitive data**: Files in `data/.sensitive/` are not tracked and must be obtained separately.

## Citation

If you use this work, please cite:

```bibtex
@article{author2024title,
  author = {Author, First and Author, Second},
  title = {Title of the Paper},
  journal = {Journal Name},
  year = {2024},
  doi = {10.xxxx/xxxxx}
}
```

## License

[Choose appropriate license]

## Contact

[Your name and contact information]

---

*This project uses the [Research Assistant Template](https://github.com/[link-to-template])*
