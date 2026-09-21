---
name: review-script
description: Reviews code for behavioural correctness, failure handling, reproducibility, testing, and scientific validity. Use for /review_script, code review, or before relying on a script in an analysis or methods section.
---

# Review code and analysis scripts

Read the target code, callers, configuration, tests, pipeline definition, and relevant scientific context.

## Review order
1. Intended behaviour and data contract
2. Correctness on realistic and edge-case inputs
3. Experimental-unit, leakage, alignment, coordinate, and parameter-propagation risks
4. Errors, silent fallbacks, skipped work, and partial outputs
5. Reproducibility: paths, seeds, dependencies, provenance, DVC inputs/outputs
6. Tests, observability, maintainability, and documentation

Verify important claims by running focused tests or small fixtures when safe. Do not equate style with correctness or require docstrings for trivial private helpers. Report findings by severity with file/line evidence, impact, and a concrete fix. Distinguish observed defects from questions and optional improvements. Do not modify files unless asked.
