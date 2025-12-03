# /write_methods Command

> Generate or update the methods section based on actual scripts in the pipeline.
> Links code directly to reproducible documentation.

## When to Use
- After completing a script in `pipeline/scripts/`
- When methods.md is out of sync with code
- Before writing results section
- As part of documentation review

## Prerequisites
- At least one script exists in `pipeline/scripts/`
- Scripts have docstrings/documentation
- dvc.yaml reflects the pipeline structure

## Common Mistakes to Avoid

1. **Vague descriptions**
   - ❌ "Samples were analyzed using standard methods"
   - ✅ "Samples were analyzed using high-performance liquid chromatography (HPLC; Agilent 1260 Infinity II, Agilent Technologies, Santa Clara, CA) with a C18 column (4.6 × 250 mm, 5 μm particle size)"

2. **Missing statistical details**
   - ❌ "Data were analyzed statistically"
   - ✅ "Group differences were analyzed using two-tailed independent samples t-tests with Welch's correction for unequal variances. Effect sizes were calculated using Cohen's d."

3. **Incomplete software information**
   - ❌ "Analysis was performed in R"
   - ✅ "Analysis was performed in R version 4.2.1 using the lme4 package (version 1.1-30) for mixed-effects models"

4. **Mixing Methods with Results**
   - Methods: What you planned to do
   - Results: What happened
   - Keep strictly separate!

5. **Insufficient sample size justification**
   - Always include power analysis or rationale
   - State actual vs. planned sample sizes if different

### What to Exclude

- Results or interpretation of results
- Justification for why the study was done (belongs in Introduction)
- Detailed literature review of methods
- Unnecessary detail about standard procedures (cite protocols instead)
- Trade names when generic names suffice

## Execution Steps

### 1. Gather Context

Read these files:
- `.research/project_telos.md` - Aims and methodology notes
- `dvc.yaml` - Pipeline stages
- `params.yaml` - Parameters used
- `pipeline/scripts/*.py` or `*.R` - All scripts
- `manuscript/methods.md` - Existing draft (if any)

### 2. Analyze Pipeline Structure

Extract from each script:
- Purpose (from docstring)
- Inputs and outputs
- Key parameters
- Dependencies/libraries used
- Algorithms/methods applied

### 3. Methods Section Structure

```markdown
# Methods

## Overview
<!-- Brief summary of analytical approach -->

## Data
### Data Sources
<!-- Where data comes from, access info -->

### Data Preprocessing
<!-- Cleaning, filtering, transformation -->

## Analysis Pipeline

### [Stage 1 Name]
<!-- What, why, how - link to script -->

### [Stage 2 Name]
<!-- Continue for each stage -->

## Statistical Analysis
<!-- Tests, thresholds, multiple testing correction -->

## Software and Reproducibility
<!-- Tools, versions, how to reproduce -->
```

### 4. Writing Standards for Methods

**Level of Detail Test**: Could another researcher reproduce your work?

| Include | Exclude |
|---------|---------|
| Parameter values used | Step-by-step code walkthrough |
| Software versions | Obvious standard operations |
| Algorithm choices with rationale | Every library imported |
| Thresholds and why they were chosen | Trivial data wrangling |
| Sample sizes at each step | Code syntax details |

**Reporting Checklist:**

For **computational methods**:
- [ ] Software name and version
- [ ] Key parameters and settings
- [ ] Random seeds (if applicable)
- [ ] Hardware specs (if relevant to runtime/reproducibility)

For **statistical analyses**:
- [ ] Test name and implementation
- [ ] Significance threshold (e.g., α = 0.05)
- [ ] Multiple testing correction method
- [ ] Effect size measures used
- [ ] Assumptions checked

For **machine learning**:
- [ ] Model type and hyperparameters
- [ ] Training/validation/test split
- [ ] Cross-validation strategy
- [ ] Evaluation metrics
- [ ] Feature selection method

### Essential Elements Checklist (Experimental Work)

For lab-based or clinical research, also include:

- [ ] Exact sample sizes and how they were determined
- [ ] Inclusion and exclusion criteria
- [ ] Randomization procedures (if applicable)
- [ ] Blinding procedures (if applicable)
- [ ] Specific equipment models and manufacturers with locations (city, country)
- [ ] Reagent catalog numbers and concentrations
- [ ] Ethical approval information (IRB/IACUC numbers)
- [ ] Informed consent procedures
- [ ] Data collection timeframes

### Reporting Guidelines by Study Type

Follow the appropriate reporting guideline:

| Study Type | Guideline | URL |
|------------|-----------|-----|
| Randomized Controlled Trials | CONSORT | consort-statement.org |
| Observational Studies | STROBE | strobe-statement.org |
| Systematic Reviews | PRISMA | prisma-statement.org |
| Diagnostic Accuracy | STARD | stard-statement.org |
| Animal Studies | ARRIVE | arriveguidelines.org |
| Qualitative Research | SRQR, COREQ | equator-network.org |
| Case Reports | CARE | care-statement.org |
| Machine Learning | TRIPOD+AI | tripod-statement.org |

*Full list at: https://www.equator-network.org/reporting-guidelines/*

### 5. Script-to-Methods Mapping

Create a mapping table:

```markdown
## Code-to-Methods Reference

| Script | Methods Section | Purpose |
|--------|-----------------|---------|
| `01_preprocess.py` | Data Preprocessing | Quality filtering, normalization |
| `02_feature_select.py` | Feature Selection | Variance-based filtering |
| `03_model_train.py` | Model Training | Random forest classification |
| `04_evaluate.py` | Evaluation | Performance metrics |
```

### 6. Generate Methods Draft

```markdown
# Methods

<!-- 
Draft generated by Research Assistant on [DATE]
Based on scripts in: pipeline/scripts/
Pipeline defined in: dvc.yaml

⚠️ VERIFY:
- All software versions are current
- Parameters match params.yaml
- Nothing critical is missing
-->

## Overview

This study employed [brief approach summary] to [achieve aim]. 
The analysis pipeline was implemented in Python [version] and 
managed using DVC for reproducibility.

## Data

### Data Sources

[Describe data sources from project_telos.md or scripts]

Data were obtained from [source]. [N] samples were included 
after quality filtering (see Data Preprocessing).

### Data Preprocessing

*Script: `pipeline/scripts/01_preprocess.py`*

[Auto-generated from script docstring and code analysis]

Raw data were processed as follows:
1. [Step 1 with parameters]
2. [Step 2 with parameters]

Samples with [condition] were excluded, resulting in [N] samples 
for downstream analysis.

## Analysis Pipeline

### [Stage Name]

*Script: `pipeline/scripts/02_analysis.py`*

[Description from docstring]

Parameters:
- Parameter 1: value (rationale)
- Parameter 2: value (rationale)

### [Continue for each pipeline stage]

## Statistical Analysis

[If applicable - describe tests used]

Differential expression analysis was performed using [method] with 
[parameters]. P-values were adjusted for multiple testing using 
[correction method] with a significance threshold of [α].

Effect sizes were calculated as [measure].

## Software and Reproducibility

All analyses were performed using:
- Python [version] with [key packages]
- R [version] with [key packages] (if applicable)
- DVC [version] for pipeline management

The complete analysis pipeline is available at [repository] and 
can be reproduced using:

```bash
dvc repro
```

---

## Code-to-Methods Reference

| Script | Section | Params |
|--------|---------|--------|
| [auto-generated table] |

## Missing Documentation Flags

[List any scripts without docstrings or unclear purposes]
```

### 7. Validation Checks

After generating, verify:

```
Methods draft created. Validation checklist:

✓ All pipeline/scripts/*.py referenced
✓ Parameters extracted from params.yaml
? Check: Are all parameter values correct?
? Check: Are software versions current?
? Check: Can a reader reproduce this?

Flagged issues:
⚠️ Script preprocessing.py lacks docstring
⚠️ params.yaml has parameters not mentioned in methods

Run /review_script preprocessing.py to add documentation.
```

### 8. Common Patterns

**For data cleaning:**
```markdown
Raw data were filtered to remove [criteria]. Quality control metrics 
included [metrics]. Samples/features with [threshold] were excluded, 
resulting in [N] retained for analysis.
```

**For normalization:**
```markdown
Data were normalized using [method] (Citation) to account for [bias type]. 
Specifically, [brief description of how method works].
```

**For model training:**
```markdown
A [model type] was trained to [task]. Hyperparameters were selected via 
[grid search/random search/etc.] with [N]-fold cross-validation. The 
final model used [list key hyperparameters with values].
```

**For evaluation:**
```markdown
Model performance was evaluated on held-out test data ([N]% of samples) 
using [metrics]. [Significance testing or confidence intervals] were 
computed using [method].
```

## Related Commands

- `/review_script [path]` - Add documentation to undocumented scripts
- `/write_results` - Next manuscript section (after figures exist)
- `/next` - Get suggestions

## Notes

- Methods should be written in past tense (you did the work)
- Be specific: "threshold of 0.5" not "appropriate threshold"
- Link to code repository in software section
- Update methods when pipeline changes
