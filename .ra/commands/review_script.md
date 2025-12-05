# /review_script Command

> Review a script for documentation quality, code standards, and reproducibility.
> Helps ensure code is ready for the methods section.

## Usage
```
/review_script [path]
/review_script pipeline/scripts/preprocessing.py
/review_script pipeline/scripts/  # Review all scripts in directory
```

## When to Use
- After writing a new script
- Before running /write_methods
- When passive checks flag undocumented scripts
- During code review or cleanup

## Execution Steps

### 1. Load Script(s)

Read the specified script or all scripts in directory.

### 2. Documentation Checklist

For each script, check:

```markdown
## Documentation Review: [script_name.py]

### Module-Level Documentation
- [ ] Has module docstring explaining purpose
- [ ] Lists author/date (optional but good)
- [ ] Describes inputs/outputs
- [ ] Notes dependencies

### Function Documentation
| Function | Has Docstring | Args Documented | Returns Documented |
|----------|---------------|-----------------|-------------------|
| func1 | ✓/✗ | ✓/✗ | ✓/✗ |
| func2 | ✓/✗ | ✓/✗ | ✓/✗ |

### Inline Comments
- [ ] Complex logic is explained
- [ ] Magic numbers are explained
- [ ] Non-obvious decisions documented

#### Inline Comment Guidance: Explain WHY, Not WHAT

```python
# ❌ BAD: States the obvious (what the code does)
x = x + 1  # Increment x by 1
data = data.dropna()  # Drop NA values

# ✅ GOOD: Explains reasoning (why we're doing it)
x = x + 1  # Offset for 1-based indexing in output file
data = data.dropna()  # Required by downstream model; NAs cause silent failures

# ❌ BAD: Obvious from context
if threshold > 0.5:  # Check if threshold is greater than 0.5

# ✅ GOOD: Explains the magic number
if threshold > 0.5:  # Optimized cutoff from ROC analysis (see supplementary Fig S2)
```

### Reproducibility
- [ ] Random seeds set (if applicable)
- [ ] Parameters configurable (not hardcoded)
- [ ] Dependencies importable
```

### 3. Code Quality Checks

```markdown
### Code Quality

**Strengths:**
- [What's done well]

**Issues:**
- 🔴 Critical: [Must fix]
- 🟡 Recommended: [Should fix]
- 🔵 Suggestion: [Nice to have]

**Examples:**
```python
# Issue: Magic number without explanation
threshold = 0.7  # TODO: document why 0.7

# Better:
threshold = 0.7  # Based on ROC analysis (see Figure S1)
```
```

### 4. Docstring Template

If missing, suggest adding:

**Python function:**
```python
def process_data(input_file: str, threshold: float = 0.5) -> pd.DataFrame:
    """
    Process raw data file and apply quality filtering.
    
    Reads the input file, removes low-quality samples, and applies
    normalization. Used as first step in the analysis pipeline.
    
    Args:
        input_file: Path to raw data CSV file
        threshold: Quality score cutoff (default: 0.5)
    
    Returns:
        DataFrame with processed samples, shape (n_samples, n_features)
    
    Raises:
        FileNotFoundError: If input_file doesn't exist
        ValueError: If threshold not in [0, 1]
    
    Example:
        >>> df = process_data("data/raw/samples.csv", threshold=0.6)
        >>> print(df.shape)
        (150, 2000)
    """
```

**Python module:**
```python
"""
Preprocessing module for RNA-seq data.

This module handles quality filtering, normalization, and batch
correction for raw count data. It is the first stage of the
analysis pipeline.

Scripts:
    - preprocess.py: Main preprocessing logic
    
Usage:
    python preprocess.py --input data/raw/counts.csv --output data/processed/

Author: [Name]
Date: [Date]
"""
```

**R function:**
```r
#' Process raw data file and apply quality filtering
#'
#' Reads the input file, removes low-quality samples, and applies
#' normalization. Used as first step in the analysis pipeline.
#'
#' @param input_file Path to raw data CSV file
#' @param threshold Quality score cutoff (default: 0.5)
#' @return DataFrame with processed samples
#' @export
#' @examples
#' df <- process_data("data/raw/samples.csv", threshold = 0.6)
process_data <- function(input_file, threshold = 0.5) {
  # Implementation
}
```

### 5. Generate Review Report

```markdown
# Script Review: [script_name]

## Summary
- Documentation: [Good/Needs work/Missing]
- Code quality: [Good/Needs work]
- Reproducibility: [Ready/Needs work]

## Documentation Status

### Module Docstring: [✓ Present / ✗ Missing]
[If missing, suggest content]

### Functions
| Function | Docstring | Quality |
|----------|-----------|---------|
| main() | ✗ Missing | Add description of entry point |
| process() | ✓ Present | Good, but add example |

## Issues Found

### 🔴 Critical (Must Fix)
1. [Issue] - Line [N]
   ```python
   # Current
   [problematic code]
   
   # Suggested
   [improved code]
   ```

### 🟡 Recommended
1. [Issue with suggestion]

### 🔵 Nice to Have
1. [Optional improvement]

## Methods Section Notes

When documenting this script in methods.md, include:
- [Key algorithm/method used]
- [Important parameters: X, Y, Z]
- [Any assumptions made]

## Quick Fixes

Copy-paste these improvements:

[Ready-to-use docstrings and comments]
```

### 6. Offer to Apply Fixes

```
Review complete. Would you like me to:

A) Add the suggested docstrings to [script_name]
B) Review another script
C) Update methods.md with this script's documentation
D) Show me the full suggested improvements

Choice?
```

## Version Control Best Practices

### Commit Message Format

Use this format for meaningful git history:

```
<type>: <subject>

<optional body>

Types:
- feat:     New feature or analysis
- fix:      Bug fix
- docs:     Documentation only
- refactor: Code restructuring (no behavior change)
- test:     Adding or updating tests
- data:     Data processing or cleaning changes
- style:    Formatting, no code change
```

**Examples:**
```bash
git commit -m "feat: Add bootstrap confidence interval calculation"
git commit -m "fix: Correct degrees of freedom in t-test"
git commit -m "docs: Add docstrings to preprocessing module"
git commit -m "data: Add outlier filtering step to pipeline"
```

### Naming Conventions

**Files:**
```
YYYYMMDD_experiment_condition_replicate.csv
2024-03-15_qpcr_treatment_01.csv
preprocess_rnaseq.py  (lowercase with underscores)
```

**Variables:**
```python
# ✅ Good: lowercase_with_underscores
subject_id, reaction_time_ms, treatment_group

# ❌ Avoid:
subjectID          # camelCase in Python
"data file.csv"    # Spaces in names
1_first_column     # Starting with numbers
```

## Quality Standards

### Documentation Levels

| Level | Description | Minimum For |
|-------|-------------|-------------|
| 1 - Minimal | Module docstring only | Personal scripts |
| 2 - Basic | + Function docstrings | Shared code |
| 3 - Complete | + Examples, types | Publication |
| 4 - Comprehensive | + Tests, edge cases | Package release |

**Target for publication: Level 3**

### Reproducibility Checklist

```markdown
## Reproducibility Review

- [ ] No hardcoded absolute paths
- [ ] All file paths use params.yaml or CLI args
- [ ] Random seeds set and documented
- [ ] Package versions in environment file
- [ ] No reliance on global state
- [ ] Outputs are deterministic
- [ ] Error messages are informative
```

### Publication-Ready Checklist

Before manuscript submission, verify:

```markdown
## Publication Reproducibility Checklist

- [ ] All analysis code in version control (git)
- [ ] Random seeds set and documented in params.yaml
- [ ] Package/environment versions recorded (requirements.txt or environment.yml)
- [ ] Data processing pipeline fully documented
- [ ] Steps to reproduce results in README
- [ ] Code archived with DOI (Zenodo/Figshare) ← Do before submission
- [ ] Code repository link included in manuscript
- [ ] CITATION.cff file created for proper attribution
```

### CITATION.cff Template

Create this file in your project root to make your code citable:

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "[Your Last Name]"
    given-names: "[Your First Name]"
    orcid: "https://orcid.org/0000-0000-0000-0000"  # Optional but recommended
  - family-names: "[Collaborator Last Name]"
    given-names: "[Collaborator First Name]"
title: "[Your Project Title]"
version: 1.0.0
date-released: YYYY-MM-DD
url: "https://github.com/username/repository"
doi: "10.5281/zenodo.XXXXXXX"  # Add after Zenodo archive
license: MIT  # Or your chosen license
repository-code: "https://github.com/username/repository"
keywords:
  - [keyword1]
  - [keyword2]
```

### Changelog Format

Maintain a CHANGELOG.md in your project:

```markdown
# Changelog

## [Unreleased]
### Added
- New feature or analysis

## [1.0.0] - YYYY-MM-DD
### Added
- Initial analysis pipeline
- Preprocessing module

### Changed
- Updated normalization method

### Fixed
- Corrected sample size calculation
```

## Related Commands

- `/write_methods` - Document script in methods section
- `/next` - Get next suggestion
- Run again with different script path

## Notes

- Good documentation now saves hours later
- Write docstrings as if explaining to a colleague
- Comments explain WHY, code explains WHAT
- Update docs when code changes
